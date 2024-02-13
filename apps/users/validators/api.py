import re


def valid_name(name):
    for char in name:
        if not char.isalpha() and not char.isspace() and not char.isnumeric():
            return False
    return True


def valid_email(email):
    model = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(\.br)?$"
    response = re.findall(model, email)
    return response


def valid_phone(phone):
    if len(phone) == 11:
        model = r"^\(?\d{2}\)?\d{5}\d{4}$"
        response = re.findall(model, phone)
        return response

    return False


def equal_passwords(password, password_confirm):
    if password != password_confirm:
        return False

    return True


def valid_password(password):
    model = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!#%*?&+=-_/,.])[A-Za-z\d@$!%#*?&+=-_/,.]{8,}$"
    response = re.findall(model, password)
    if response:
        return True

    return False
