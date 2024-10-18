import csv
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from time_period import TimePeriod

MIN_REQUEST_NOTICE_IN_DAYS = 60
LOOKBACK_PERIOD_IN_MONTHS = 12
MAX_DAYS_IN_LOOKBACK_PERIOD = 30
TODAY = date.today()
DATE_FORMAT = "yyyy-mm-dd"


def debug():
    pass


def convert_to_date(string_date):
    converted_date = datetime.strptime(string_date, "%Y-%m-%d").date()
    return converted_date


def calculate_earliest_date():
    earliest_international_working_date = TODAY + timedelta(days=MIN_REQUEST_NOTICE_IN_DAYS)
    print(
        f"Earliest possible international working date (if request submitted today): {earliest_international_working_date}\n")


def calculate_deadline():
    print("\nCalculate request submission deadline\n".upper())

    start_date = convert_to_date(
        input(f"What is the start date of your proposed international working period ({DATE_FORMAT})? "))
    request_deadline = start_date - timedelta(days=MIN_REQUEST_NOTICE_IN_DAYS)
    print(f"The last day to submit the international working request is {request_deadline}.")
    input("Press enter to continue. ")
    print("\n\n")


def check_eligibility(max_period):
    """display current status and check eligibility given a proposed new international working period"""

    print("\nCheck eligibility of a proposed international working period\n".upper())

    relevant_international_working_periods = []
    total_no_of_days_in_lookback_period = 0

    # get proposed period from user
    proposed_period = TimePeriod()
    relevant_international_working_periods.append(proposed_period)

    # calculate (start_date - 12 months) to get start date of lookback period
    lookback_period_start_date = proposed_period.start_date - relativedelta(months=LOOKBACK_PERIOD_IN_MONTHS)

    # get data from csv file
    international_working_periods = []

    with open("international_working_periods.csv", newline="") as iwp_data:
        time_periods_reader = csv.reader(iwp_data, delimiter=",", quotechar="|")
        next(time_periods_reader, None)  # skip headers
        for row in time_periods_reader:
            new_period = [convert_to_date(col) for col in row]
            international_working_periods.append(new_period)

    # pre-check - check if no of days between (start_date - 12 months) and end_date exceeds allowance
    international_working_periods_in_lookback_period = [period for period in international_working_periods if
                                                        period[0] >= lookback_period_start_date]

    for period in international_working_periods_in_lookback_period:
        new_time_period = TimePeriod(start_date=period[0], end_date=period[1])
        relevant_international_working_periods.append(new_time_period)

    for period in relevant_international_working_periods:
        days_in_period = period.calculate_no_of_days()
        total_no_of_days_in_lookback_period += days_in_period

    # user feedback based on outcome of pre-check
    if total_no_of_days_in_lookback_period <= MAX_DAYS_IN_LOOKBACK_PERIOD:
        print(f"""
    ✅ Including the proposed international working period, you would have a maximum of 
    {total_no_of_days_in_lookback_period} working days booked within 12 months, which does not exceed the allowance 
    of {MAX_DAYS_IN_LOOKBACK_PERIOD} days.\n
        """)
        wants_to_record = input("Would you like to add this new international working period to the records? (y/n) ")
        if wants_to_record == 'y':
            with open("international_working_periods.csv", "a", newline="") as records:
                records.write(f"\n{proposed_period.start_date},{proposed_period.end_date}")
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


def add_new_period():
    """Ask for start and end date of the new international working period and add them to data file"""

    print("\nRecord new international working period\n".upper())

    start_date = input(f"Enter the start date of the new international working period ({DATE_FORMAT}): ")
    end_date = input(f"Enter the end date of the new international working period ({DATE_FORMAT}): ")

    with open("international_working_periods.csv", "a", newline="") as records:
        records.write(f"\n{start_date},{end_date}")

    input("Press enter to continue. ")
    print("\n\n")


print("INTERNATIONAL WORKING REQUEST CALCULATOR\n")

run_calculator = True

while run_calculator == True:
    print(f"Today's date: {TODAY}")
    calculate_earliest_date()

    print(f"""
    1. Calculate request submission deadline based on a desired start date
    2. Check whether a proposed international working period complies with the {MAX_DAYS_IN_LOOKBACK_PERIOD}-day rule
    3. Record a new international working period
    4. Exit
    """)

    choice = int(input("Please choose one of the options above: "))

    match choice:
        case 1:
            calculate_deadline()
        case 2:
            check_eligibility(max_period=MAX_DAYS_IN_LOOKBACK_PERIOD)
        case 3:
            add_new_period()
        case 4:
            run_calculator = False
        case 5:
            debug()
        case _:
            pass
