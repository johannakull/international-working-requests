import constants as c
import utils as u


print("INTERNATIONAL WORKING REQUEST CALCULATOR\n")

print(f"Today's date: {c.TODAY}")
u.calculate_earliest_date()

while True:
    print(f"""
    1. Calculate request submission deadline based on a desired start date
    2. Check whether a proposed international working period complies with the {c.MAX_DAYS_IN_LOOKBACK_PERIOD}-day rule
    3. Record a new international working period
    4. Exit
    """)

    try:
        choice = int(input("Please choose one of the options above: "))
        while choice not in (1, 2, 3, 4):
            choice = int(input("That is not one of the available options. Please choose one of the options above: "))
        match choice:
            case 1:
                u.calculate_deadline()
            case 2:
                u.check_eligibility()
            case 3:
                u.add_new_period()
            case 4:
                break
    except ValueError:
        print("Invalid input. Please choose one of the available options.")
