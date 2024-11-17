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
    wait_for_key_press()


def check_eligibility():
    """display current status and check eligibility given a proposed new international working period"""

    relevant_periods = []  # all periods that require 12-months check

    print("\nCheck eligibility of a proposed international working period\n".upper())

    while True:
        proposed_period_start_date = convert_to_date(input(f"Enter a proposed start date ({c.DATE_FORMAT}): "))
        proposed_period_end_date = convert_to_date(input(f"Enter a proposed end date ({c.DATE_FORMAT}): "))

        if check_date_input_validity(proposed_period_start_date, proposed_period_end_date):
            break
        else:
            print("\nEnd date cannot be before start date.\n")

    # Pre-check - if proposed period exceeds allowance on its own, do not proceed with eligibility check
    days_in_proposed_period = get_dates_in_range(proposed_period_start_date, proposed_period_end_date)
    if len(days_in_proposed_period) > c.MAX_DAYS_IN_LOOKBACK_PERIOD:
        print(f"\n❌ The proposed period exceeds the allowance of {c.MAX_DAYS_IN_LOOKBACK_PERIOD} days.")
        wait_for_key_press()
        return

    relevant_periods.append((proposed_period_start_date, proposed_period_end_date))

    # calculate start & end date of relevant range (proposed start_date - 12 months, proposed_end_date + 12 months)
    first_relevant_date = proposed_period_start_date - relativedelta(months=c.LOOKBACK_PERIOD_IN_MONTHS)
    last_relevant_date = proposed_period_end_date + relativedelta(months=c.LOOKBACK_PERIOD_IN_MONTHS)

    # get any periods from data file that lie in or overlap with relevant range & trim if required
    with open("international_working_days.csv", newline="") as international_working_data:
        dates_reader = csv.reader(international_working_data, delimiter=",", quotechar="|")
        for row in dates_reader:
            current_period_start_date = convert_to_date(row[0])
            current_period_end_date = convert_to_date(row[1])
            # check if the current period lies in or overlaps with the relevant range
            if current_period_end_date >= first_relevant_date and current_period_start_date <= last_relevant_date:
                # if so, determine which days of the current period lie within the relevant range and add them to
                # trimmed range - split this into separate function for readability
                current_date_range = get_dates_in_range(current_period_start_date, current_period_end_date)
                new_date_range = [date for date in current_date_range if first_relevant_date <= date <= last_relevant_date]
                # add new, trimmed period's start and end dates to relevant periods
                relevant_periods.append((new_date_range[0], new_date_range[-1]))

    relevant_periods.sort()

    # create new list with all dates that fall into the relevant periods
    dates_in_relevant_periods = []
    for period in relevant_periods:
        dates_in_period = get_dates_in_range(period[0], period[1])
        for date in dates_in_period:
            dates_in_relevant_periods.append(date)

    # for each relevant period, check if there are more than 30 days booked in the next 12 months
    for period in relevant_periods:
        start_date_for_check = period[0]
        end_date_for_check = start_date_for_check + relativedelta(months=c.LOOKBACK_PERIOD_IN_MONTHS)
        dates_in_current_check_period = [date for date in dates_in_relevant_periods if start_date_for_check <= date <= end_date_for_check]
        if len(dates_in_current_check_period) > c.MAX_DAYS_IN_LOOKBACK_PERIOD:
            print(
                f"❌ The proposed period would exceed the allowance of {c.MAX_DAYS_IN_LOOKBACK_PERIOD} days when combined with your other international working periods.")
            break
    else:
        print(f"✅ The proposed period does not exceed the allowance of {c.MAX_DAYS_IN_LOOKBACK_PERIOD} days.")
        wants_to_record = input("Would you like to add this new international working period to the records? (y/n) ")
        if wants_to_record == 'y':
            write_dates_to_file(proposed_period_start_date, proposed_period_end_date)

    wait_for_key_press()


def add_new_period():
    """Ask for start and end date of the new international working period and add them to data file"""

    print("\nRecord new international working period\n".upper())

    start_date = convert_to_date(
        input(f"Enter the start date of the new international working period ({c.DATE_FORMAT}): "))
    end_date = convert_to_date(input(f"Enter the end date of the new international working period ({c.DATE_FORMAT}): "))
    new_dates = get_dates_in_range(start_date, end_date)

    write_dates_to_file(new_dates)
    wait_for_key_press()


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


def write_dates_to_file(start_date, end_date):
    with open("international_working_days.csv", "a", newline="") as records:
        records.write(f"{start_date},{end_date}\n")
    print("\nNew date(s) recorded successfully.")


def wait_for_key_press():
    input("\nPress enter to continue. ")


def check_date_input_validity(first_date, second_date):
    if second_date < first_date:
        return False
    return True
