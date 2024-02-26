from datetime import date


def retroactive_date(input_date):
    if input_date < date.today():
        return False

    return True
