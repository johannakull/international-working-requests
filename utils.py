import csv
import constants as c
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def get_dates_in_range(start_date, end_date):
    """returns a list of dates in a specified range"""
    dates_in_range = []
    delta = timedelta(days=1)
    date = start_date
    while date <= end_date:
        dates_in_range.append(date)
        date += delta
    return dates_in_range


def write_dates_to_file(dates):
    with open("international_working_days.csv", "a", newline="") as records:
        for date in dates:
            records.write(f"{date}\n")
    print("New date(s) recorded successfully.")

def add_new_period():
    """Ask for start and end date of the new international working period and add them to data file"""

    print("\nRecord new international working period\n".upper())

    start_date = convert_to_date(input(f"Enter the start date of the new international working period ({c.DATE_FORMAT}): "))
    end_date = convert_to_date(input(f"Enter the end date of the new international working period ({c.DATE_FORMAT}): "))
    new_dates = get_dates_in_range(start_date, end_date)

    write_dates_to_file(new_dates)

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


    # 1. PRE-CHECK - check if no of days between (start_date - 12 months) and end_date exceeds allowance
    # 1.1 get proposed new period from user and add it to list of days in relevant period
    start_date = convert_to_date(input(f"Enter a proposed start date ({c.DATE_FORMAT}): "))
    end_date = convert_to_date(input(f"Enter a proposed end date ({c.DATE_FORMAT}): "))
    new_dates = get_dates_in_range(start_date, end_date)

    relevant_dates = [date for date in new_dates]

    # 1.2 calculate start of relevant period (proposed start_date - 12 months)
    relevant_period_start_date = relevant_dates[0] - relativedelta(months=c.LOOKBACK_PERIOD_IN_MONTHS)

    # 1.3 add previously recorded IWPs from data file that fall into relevant period to list of relevant days
    with open("international_working_days.csv", newline="") as iwp_data:
        time_periods_reader = csv.reader(iwp_data, delimiter=",", quotechar="|")
        for row in time_periods_reader:
            date = convert_to_date(row[0])
            if relevant_period_start_date <= date <= end_date:
                relevant_dates.append(date)

    # 1.4 check if no of days between (start_date - 12 months) and end_date exceeds allowance & output feedback to user
    total_days_in_relevant_period = len(relevant_dates)
    if total_days_in_relevant_period <= 30:
        print(f"""
        ✅ Including the proposed international working period, you would have a maximum of
        {total_days_in_relevant_period} working days booked within 12 months, which does not exceed the allowance
        of {c.MAX_DAYS_IN_LOOKBACK_PERIOD} days.\n
        """)
        wants_to_record = input("Would you like to add this new international working period to the records? (y/n) ")
        if wants_to_record == 'y':
            write_dates_to_file(new_dates)
        else:
            print("The new international working period was not added to the records. Remember to add it once booked.")
    else:
        for date in new_dates:
            lookback_date = date - relativedelta(months=c.LOOKBACK_PERIOD_IN_MONTHS) + timedelta(days=1)
            dates_in_lookback_period = [day for day in relevant_dates if day >= lookback_date]
            if len(dates_in_lookback_period) > 30:  # TODO: calculate date proposed period would have to shift to or number of days to cut to be eligible
                print(f"""
                ❌ The proposed period exceeds the allowance of {c.MAX_DAYS_IN_LOOKBACK_PERIOD} days
                in any {c.LOOKBACK_PERIOD_IN_MONTHS} months.
                """)
                break
        else:
            print(f"""
            ✅ The proposed period does not exceed the allowance of {c.MAX_DAYS_IN_LOOKBACK_PERIOD} days
            in any {c.LOOKBACK_PERIOD_IN_MONTHS} months.
            """)

    input("Press enter to continue. ")
    print("\n\n")


def convert_to_date(string_date):
    converted_date = datetime.strptime(string_date, "%Y-%m-%d").date()
    return converted_date
