from datetime import date, datetime


def retroactive_date(input_date):
    print(type(input_date))
    today = date.today()
    if isinstance(input_date, datetime):
        print("é instancia datetime")
        input_date = input_date.date()
        
    if input_date < today:
        return False

    return True

