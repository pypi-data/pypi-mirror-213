import re


def validator(f):
    def validate_email(*args):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, args[1]):
            return f(*args)
        else:
            raise ValueError(f"{args[1]} does not appear valid email")

    return validate_email
