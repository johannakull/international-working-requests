import datetime

MIN_REQUEST_PERIOD_IN_DAYS = 60
MAX_DAYS_IN_YEAR = 30
TODAY = datetime.date.today()
DATE_FORMAT = "yyyy-mm-dd"


def calculate_earliest_date():
    earliest_international_working_date = TODAY + datetime.timedelta(days=MIN_REQUEST_PERIOD_IN_DAYS)
    print(f"Earliest possible international working date (if request submitted today): {earliest_international_working_date}\n")


def calculate_deadline():
    start_date = datetime.datetime.strptime(input("What is the start data of your proposed international working period? "),
                                            "%Y-%m-%d").date()
    request_deadline = start_date - datetime.timedelta(days=MIN_REQUEST_PERIOD_IN_DAYS)
    print(f"The last day to submit the international working request is {request_deadline}.")


def check_eligibility(max_period):
    current_period = 31     # TODO1: check no of days
    print(f"\nYou currently have {current_period} working days booked within 12 months.")
    if current_period > MAX_DAYS_IN_YEAR:
        print(f"""❌ You currently exceed the number of allowed international working days ({MAX_DAYS_IN_YEAR}) 
in any 12-month period.""")
    else:
        print(f"""✅ You do not currently exceed the number of allowed international working days ({MAX_DAYS_IN_YEAR}) 
in any 12-month period.""")
    proposed_start_date = input(f"Enter a proposed start date ({DATE_FORMAT}): ")
    proposed_end_date = input(f"Enter a proposed end date ({DATE_FORMAT}): ")
    #TODO3: add proposed period to current_period and check whether total period exceeds max allowed days


def add_new_period():
    """Ask for start and end date of the new international working period and add them to data file"""

    start_date = input(f"Enter the start date of the new international working period ({DATE_FORMAT}): ")
    end_date = input(f"Enter the end date of the new international working period ({DATE_FORMAT}): ")

    with open("international_working_periods.csv", "a", newline="") as records:
        records.write(f"\n{start_date},{end_date}")

print("INTERNATIONAL WORKING REQUEST CALCULATOR\n")
print(f"Today's date: {TODAY}")

calculate_earliest_date()

print(f"""
1. Calculate request submission deadline based on a desired start date
2. Check whether a proposed international working period complies with the {MAX_DAYS_IN_YEAR}-day rule
3. Record a new international working period
""")

choice = int(input("Please choose one of the options above: "))

if choice == 1:
    calculate_deadline()
elif choice == 2:
    check_eligibility(max_period=MAX_DAYS_IN_YEAR)
elif choice == 3:
    add_new_period()
else:
    pass
