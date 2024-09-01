import datetime

MIN_REQUEST_PERIOD = 60

today = datetime.date.today()

print("INTERNATIONAL WORKING REQUESTS CALCULATOR\n")
print(f"Today's date: {today}")

earliest_international_working_date = today + datetime.timedelta(days=MIN_REQUEST_PERIOD)
print(f"Earliest possible international working date (if request submitted today): {earliest_international_working_date}\n")

start_date = datetime.datetime.strptime(input("What is the start data of your proposed international working period? "), "%Y-%m-%d").date()
request_deadline = start_date - datetime.timedelta(days=MIN_REQUEST_PERIOD)
print(f"The last day to submit the international working request is {request_deadline}.")
