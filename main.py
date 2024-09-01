import datetime

MIN_REQUEST_PERIOD_IN_DAYS = 60
MAX_DAYS_IN_YEAR = 30
TODAY = datetime.date.today()


def calculate_earliest_date():
    earliest_international_working_date = TODAY + datetime.timedelta(days=MIN_REQUEST_PERIOD_IN_DAYS)
    print(f"Earliest possible international working date (if request submitted today): {earliest_international_working_date}\n")


def calculate_deadline():
    start_date = datetime.datetime.strptime(input("What is the start data of your proposed international working period? "),
                                            "%Y-%m-%d").date()
    request_deadline = start_date - datetime.timedelta(days=MIN_REQUEST_PERIOD_IN_DAYS)
    print(f"The last day to submit the international working request is {request_deadline}.")


def check_eligibility(max_period):
    pass # TODO: implement this


print("INTERNATIONAL WORKING REQUEST CALCULATOR\n")
print(f"Today's date: {TODAY}")

calculate_earliest_date()

print(f"""
1. Calculate request submission deadline based on a desired start date
2. Check whether a proposed international working period complies with the {MAX_DAYS_IN_YEAR}-day rule
3. ...
""")

choice = int(input("Please choose one of the options above: "))

if choice == 1:
    calculate_deadline()
elif choice == 2:
    check_eligibility(max_period=MAX_DAYS_IN_YEAR)
else:
    pass
