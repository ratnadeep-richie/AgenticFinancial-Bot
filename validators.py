import re

def valid_name(name):
    return bool(re.fullmatch(r"[A-Za-z ]{2,}", name))

def valid_username(username):
    return (
        re.search(r"[A-Z]", username)
        and re.search(r"[0-9]", username)
        and re.search(r"[@#$%^&*!]", username)
    )

def valid_email(email):
    return bool(re.fullmatch(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", email))

def valid_phone(phone):
    return bool(re.fullmatch(r"[6-9][0-9]{9}", phone))
