import datetime

MIN_REQUEST_PERIOD = 60

today = datetime.date.today()

print("INTERNATIONAL WORKING REQUESTS CALCULATOR\n")
print(f"Today's date: {today}")

request_deadline = today + datetime.timedelta(days=MIN_REQUEST_PERIOD)
print(f"Earliest possible international working date (if request submitted today): {request_deadline}")


