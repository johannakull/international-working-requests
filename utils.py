import csv
import constants as c
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from time_period import TimePeriod


def add_new_period():
    """Ask for start and end date of the new international working period and add them to data file"""

    print("\nRecord new international working period\n".upper())

    start_date = input(f"Enter the start date of the new international working period ({c.DATE_FORMAT}): ")
    end_date = input(f"Enter the end date of the new international working period ({c.DATE_FORMAT}): ")

    with open("international_working_periods.csv", "a", newline="") as records:
        records.write(f"\n{start_date},{end_date}")

    input("Press enter to continue. ")
    print("\n\n")


def calculate_deadline():
    print("\nCalculate request submission deadline\n".upper())

    start_date = convert_to_date(
        input(f"What is the start date of your proposed international working period ({c.DATE_FORMAT})? "))
    request_deadline = start_date - timedelta(days=c.MIN_REQUEST_NOTICE_IN_DAYS)
    print(f"The last day to submit the international working request is {request_deadline}.")
    input("Press enter to continue. ")
    print("\n\n")


def calculate_earliest_date():
    earliest_international_working_date = c.TODAY + timedelta(days=c.MIN_REQUEST_NOTICE_IN_DAYS)
    print(
        f"Earliest possible international working date (if request submitted today): {earliest_international_working_date}\n")


def check_eligibility():
    """display current status and check eligibility given a proposed new international working period"""

    print("\nCheck eligibility of a proposed international working period\n".upper())

    iwps_in_relevant_period = []
    total_days_in_relevant_period = 0

    # 1. PRE-CHECK - check if no of days between (start_date - 12 months) and end_date exceeds allowance
    # 1.1 get proposed new period from user and add it to list of IWPs in relevant period
    proposed_new_iwp = TimePeriod()
    iwps_in_relevant_period.append(proposed_new_iwp)

    # 1.2 calculate start of relevant period (proposed start_date - 12 months)
    relevant_period_start_date = proposed_new_iwp.start_date - relativedelta(months=c.LOOKBACK_PERIOD_IN_MONTHS)

    # 1.3 get previously recorded IWPs from data file
    previously_recorded_iwps = []

    with open("international_working_periods.csv", newline="") as iwp_data:
        time_periods_reader = csv.reader(iwp_data, delimiter=",", quotechar="|")
        next(time_periods_reader, None)  # skip headers
        for row in time_periods_reader:
            new_period = tuple(convert_to_date(col) for col in row)
            previously_recorded_iwps.append(new_period)

    # 1.4 add previously recorded IWPs within relevant period to list of IWPs in relevant period - BUG: currently
    # doesn't count periods that start before, but overlap with relevant period start date
    previously_recorded_iwps_in_relevant_period = [period for period in previously_recorded_iwps
                                                   if period[0] >= relevant_period_start_date]

    for period in previously_recorded_iwps_in_relevant_period:
        new_time_period = TimePeriod(start_date=period[0], end_date=period[1])
        iwps_in_relevant_period.append(new_time_period)

    # 1.5 check if no of days between (start_date - 12 months) and end_date exceeds allowance & output feedback to user
    for period in iwps_in_relevant_period:
        days_in_period = period.calculate_no_of_days()
        total_days_in_relevant_period += days_in_period

    if total_days_in_relevant_period <= c.MAX_DAYS_IN_LOOKBACK_PERIOD:
        print(f"""
    ✅ Including the proposed international working period, you would have a maximum of 
    {total_days_in_relevant_period} working days booked within 12 months, which does not exceed the allowance 
    of {c.MAX_DAYS_IN_LOOKBACK_PERIOD} days.\n
        """)
        wants_to_record = input("Would you like to add this new international working period to the records? (y/n) ")
        if wants_to_record == 'y':
            with open("international_working_periods.csv", "a", newline="") as records:
                records.write(f"\n{proposed_new_iwp.start_date},{proposed_new_iwp.end_date}")
            print("New international working period recorded successfully.")
        else:
            print("The new international working period was not added to the records. Remember to add it once booked.")
    else:
        print("Further checks needed.")

    # detailed check:
    # for day in proposed period:
    #   if [days in [(day-12 months) in datafile + days in new_period[:day]] > 30:
    #       throw error
    #   else continue

    input("Press enter to continue. ")
    print("\n\n")


def convert_to_date(string_date):
    converted_date = datetime.strptime(string_date, "%Y-%m-%d").date()
    return converted_date
