import re
from validate_docbr import CNPJ, CPF
from django.core.exceptions import ValidationError


def valid_name(name):
    for char in name:
        if not char.isalpha() and not char.isspace() and not char.isnumeric():
            raise ValidationError("Compound name shouldnt contain symbols!", "invalid")


def valid_email(email):
    model = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(\.br)?$"
    response = re.findall(model, email)
    if not response:
        return ValidationError("Invalid email!", "invalid")


def valid_phone(phone):
    model = r"^\(?\d{2}\)?\d{5}\d{4}$"
    response = re.findall(model, phone)
    if not response:
        return ValidationError(
            "O número de celular deve seguir o padrão: (XX) 9XXXX-XXXX!", "invalid"
        )

    return ValidationError("Número inválido!", "invalid")


def valid_password(password):
    model = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%#*?&+=-_/,.])[A-Za-z\d@$!%*#?&+=-_/,.]{8,}$"
    if len(password) < 8:
        raise ValidationError(
            "This password is too short. It must contain at least 8 characters.",
            code="password_too_short",
        )

    if password.isdigit():
        raise ValidationError(
            "This password is entirely numeric.", code="password_entirely_numeric"
        )

    if not re.findall(model, password):
        raise ValidationError(
            "This password must contain at least one lowercase letter, one uppercase letter, one digit, and one special character.",
            code="password_invalid",
        )
