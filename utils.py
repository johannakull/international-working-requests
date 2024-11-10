import csv
import constants as c
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def calculate_earliest_date():
    earliest_international_working_date = c.TODAY + timedelta(days=c.MIN_REQUEST_NOTICE_IN_DAYS)
    print(f"Earliest possible international working date (if request submitted today): {earliest_international_working_date}\n")


def calculate_deadline():
    print("\nCalculate request submission deadline\n".upper())

    try:
        start_date = convert_to_date(
            input(f"What is the start date of your proposed international working period ({c.DATE_FORMAT})? "))
        request_deadline = start_date - timedelta(days=c.MIN_REQUEST_NOTICE_IN_DAYS)
        print(f"The last day to submit the international working request is {request_deadline}.")
    except ValueError:
        print(f"Incorrect date format. Dates should be entered in the following format: {c.DATE_FORMAT}")
    wait_to_continue()


def check_eligibility():
    """display current status and check eligibility given a proposed new international working period"""

    print("\nCheck eligibility of a proposed international working period\n".upper())

    proposed_period_start_date = convert_to_date(input(f"Enter a proposed start date ({c.DATE_FORMAT}): "))
    proposed_period_end_date = convert_to_date(input(f"Enter a proposed end date ({c.DATE_FORMAT}): "))
    new_dates = get_dates_in_range(proposed_period_start_date, proposed_period_end_date)

    print()

    # Pre-check - if proposed period exceeds allowance on its own, do not proceed to eligibility check
    if len(new_dates) > c.MAX_DAYS_IN_LOOKBACK_PERIOD:
        print(f"❌ The proposed period exceeds the allowance of {c.MAX_DAYS_IN_LOOKBACK_PERIOD} days.")
        wait_to_continue()
        return

    relevant_dates = [date for date in new_dates]

    # calculate start of relevant period (proposed start_date - 12 months)
    first_relevant_date = proposed_period_start_date - relativedelta(months=c.LOOKBACK_PERIOD_IN_MONTHS)
    print(f"Based on the proposed start date of {proposed_period_start_date}, the first relevant date is {first_relevant_date}")

    # add previously recorded international working dates from data file that fall into relevant period
    with open("international_working_days.csv", newline="") as international_working_data:
        dates_reader = csv.reader(international_working_data, delimiter=",", quotechar="|")
        for row in dates_reader:
            current_period_start_date = convert_to_date(row[0])
            current_period_end_date = convert_to_date(row[1])
            # if date1 >= first_relevant_date or date2 >= first_relevant_date:
            # check the end date of the current period to determine if it lies in the relevant range
            if first_relevant_date <= current_period_end_date <= proposed_period_end_date:
                date_range = get_dates_in_range(current_period_start_date, current_period_end_date)
                for date in date_range:
                    if first_relevant_date <= date <= proposed_period_end_date:
                        relevant_dates.append(date)

    # check if total no of days in relevant period exceeds allowance
    lookback_date = first_relevant_date
    for _ in new_dates:
        dates_in_lookback_period = [day for day in relevant_dates if day >= lookback_date]
        if len(dates_in_lookback_period) > c.MAX_DAYS_IN_LOOKBACK_PERIOD:
            no_of_days_exceeding_allowance = len(dates_in_lookback_period) - 30
            shifted_start_date = proposed_period_start_date + timedelta(days=no_of_days_exceeding_allowance)
            shifted_end_date = proposed_period_end_date - timedelta(days=no_of_days_exceeding_allowance)
            print(
                f"❌ The proposed period would exceed the allowance of {c.MAX_DAYS_IN_LOOKBACK_PERIOD} days when combined with previously booked international working periods.")
            print(
                f"Consider shifting your start date by {no_of_days_exceeding_allowance} day(s) to {shifted_start_date} or returning to the UK {no_of_days_exceeding_allowance} day(s) earlier, on {shifted_end_date}.")
            break
        else:
            lookback_date + timedelta(days=1)
    else:
        print(f"✅ The proposed period does not exceed the allowance of {c.MAX_DAYS_IN_LOOKBACK_PERIOD} days.")
        wants_to_record = input("Would you like to add this new international working period to the records? (y/n) ")
        if wants_to_record == 'y':
            write_dates_to_file(new_dates)
    wait_to_continue()


def add_new_period():
    """Ask for start and end date of the new international working period and add them to data file"""

    print("\nRecord new international working period\n".upper())

    start_date = convert_to_date(
        input(f"Enter the start date of the new international working period ({c.DATE_FORMAT}): "))
    end_date = convert_to_date(input(f"Enter the end date of the new international working period ({c.DATE_FORMAT}): "))
    new_dates = get_dates_in_range(start_date, end_date)

    write_dates_to_file(new_dates)
    wait_to_continue()


def convert_to_date(string_date):
    converted_date = datetime.strptime(string_date, "%Y-%m-%d").date()
    return converted_date


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
    print("\nNew date(s) recorded successfully.")


def wait_to_continue():
    input("\nPress enter to continue. ")
