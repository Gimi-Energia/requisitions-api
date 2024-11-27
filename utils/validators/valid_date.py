from datetime import date, datetime


def retroactive_date(input_date):
    today = date.today()
    if isinstance(input_date, datetime):
        today = datetime.now()
        
    if input_date < today:
        return False

    return True
