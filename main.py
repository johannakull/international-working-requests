import datetime
from time_period import TimePeriod

MIN_REQUEST_PERIOD_IN_DAYS = 60
MAX_DAYS_IN_YEAR = 30
TODAY = datetime.date.today()
DATE_FORMAT = "yyyy-mm-dd"


def debug():
    pass


def convert_to_date(string_date):
    converted_date = datetime.datetime.strptime(string_date, "%Y-%m-%d").date()
    return converted_date


def calculate_earliest_date():
    earliest_international_working_date = TODAY + datetime.timedelta(days=MIN_REQUEST_PERIOD_IN_DAYS)
    print(f"Earliest possible international working date (if request submitted today): {earliest_international_working_date}\n")


def calculate_deadline():
    print("\nCalculate request submission deadline\n".upper())

    start_date = convert_to_date(input(f"What is the start date of your proposed international working period ({DATE_FORMAT})? "))
    request_deadline = start_date - datetime.timedelta(days=MIN_REQUEST_PERIOD_IN_DAYS)
    print(f"The last day to submit the international working request is {request_deadline}.")
    input("Press enter to continue. ")
    print("\n\n")


def check_eligibility(max_period):
    """display current status and check eligibility given a proposed new international working period"""

    current_period = 29     # TODO1: check actual no of days

    print("\nCheck eligibility of a proposed international working period\n".upper())
    print(f"Current status:\n")
    if current_period > MAX_DAYS_IN_YEAR:
        print(f"""❌ You currently have {current_period} working days booked within 12 months, which exceeds the
    allowance of {MAX_DAYS_IN_YEAR} days.\n""")
    else:
        print(f"""✅ You currently have {current_period} working days booked within 12 months, which does not exceed
    exceed the allowance of {MAX_DAYS_IN_YEAR} days.\n""")

    proposed_period = TimePeriod()
    proposed_period_length = proposed_period.calculate_no_of_days()
    print(proposed_period_length)
    #TODO3: add proposed period to current_period and check whether total period exceeds max allowed days
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