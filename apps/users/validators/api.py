import re
from validate_docbr import CNPJ, CPF

def valid_document(document):
    if len(document) == 14:
        return CNPJ().validate(document)
    
    if len(document) == 11:
        return CPF().validate(document)
    
    return False

def valid_name(name):
    for char in name:
        if not char.isalpha() and not char.isspace() and not char.isnumeric():
            return False
    return True

def valid_phone(phone):
    if len(phone) == 11:
        model = r'^\(?\d{2}\)?\d{5}\d{4}$'
        response = re.findall(model, phone)
        return response

    if len(phone) == 10:
        model = r'^\(?\d{2}\)?\d{4}\d{4}$'
        response = re.findall(model, phone)
        return response
    
    return False

def valid_email(email):
    model = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(\.br)?$"
    response = re.findall(model, email)
    return response

def equal_passwords(password, password_confirm):
    if password != password_confirm:
        return False
    
    return True

def valid_password(password):
    model = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&+=-_/,.])[A-Za-z\d@$!%*?&+=-_/,.]{8,}$"
    response = re.findall(model, password)
    if response:
        return True

    return False
    