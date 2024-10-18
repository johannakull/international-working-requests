import csv
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from time_period import TimePeriod

MIN_REQUEST_NOTICE_IN_DAYS = 60
MAX_DAYS_IN_YEAR = 30
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

    # get proposed period from user
    proposed_period = TimePeriod()
    days_in_proposed_period = proposed_period.calculate_no_of_days()

    # calculate (start_date - 12 months)
    max_period_from_start_date = proposed_period.start_date - relativedelta(months=12)
    print(max_period_from_start_date)

    # get data from csv file
    international_working_periods = []

    with open("international_working_periods.csv", newline="") as iwp_data:
        time_periods_reader = csv.reader(iwp_data, delimiter=",", quotechar="|")
        next(time_periods_reader, None)  # skip headers
        for row in time_periods_reader:
            new_period = [convert_to_date(col) for col in row]
            international_working_periods.append(new_period)

        print(international_working_periods)

    # get no of days in time periods from csv file


    # pre-check - check if no of days between (start_date - 12 months) and end_date exceeds allowance


    # pre check - check if no of days in [start_date-12 months : end_date] is > 30 days
    # if no - all good, period is eligible
    # if yes - do detailed check:
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
    2. Check whether a proposed international working period complies with the {MAX_DAYS_IN_YEAR}-day rule
    3. Record a new international working period
    4. Exit
    """)

    choice = int(input("Please choose one of the options above: "))

    match choice:
        case 1:
            calculate_deadline()
        case 2:
            check_eligibility(max_period=MAX_DAYS_IN_YEAR)
        case 3:
            add_new_period()
        case 4:
            run_calculator = False
        case 5:
            debug()
        case _:
            pass
