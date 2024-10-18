import datetime

DATE_FORMAT = "yyyy-mm-dd"


def convert_to_date(string_date):
    converted_date = datetime.datetime.strptime(string_date, "%Y-%m-%d").date()
    return converted_date


class TimePeriod():
    def __init__(self, start_date=None, end_date=None):
        if start_date is None:
            self.start_date = convert_to_date(input(f"Enter a proposed start date ({DATE_FORMAT}): "))
        else:
            self.start_date = start_date
        if end_date is None:
            self.end_date = convert_to_date(input(f"Enter a proposed end date ({DATE_FORMAT}): "))
        else:
            self.end_date = end_date

    def calculate_no_of_days(self):
        no_of_days = (self.end_date - self.start_date).days + 1
        return no_of_days
