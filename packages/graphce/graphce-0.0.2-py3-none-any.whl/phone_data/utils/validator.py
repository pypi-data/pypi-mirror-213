import phonenumbers
from phone_data.exceptions import InvalidPhoneException


def validator(f):
    def validate_phone(*args):
        try:
            number = phonenumbers.parse(args[1])
            if phonenumbers.is_valid_number(number):
                return f(*args)
            else:
                raise InvalidPhoneException()
        except phonenumbers.phonenumberutil.NumberParseException:
            raise InvalidPhoneException()

    return validate_phone
