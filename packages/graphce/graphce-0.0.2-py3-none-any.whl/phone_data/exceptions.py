class InvalidPhoneException(Exception):
    def __init__(self):
        super().__init__("phone number does not appear valid")
