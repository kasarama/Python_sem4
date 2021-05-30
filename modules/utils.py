import re


def validate_pass_with_regex(password):
    
    if re.fullmatch("^(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*_0-9])(.{8,})$", password):
        return True
    else:
        return False

