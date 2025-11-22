import re

class Validator:

    @staticmethod
    def valid_email(email):
        if not email:
            return False
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None

    @staticmethod
    def valid_amount(amount):
        try:
            amount = float(amount)
            return amount > 0
        except:
            return False

    @staticmethod
    def not_empty(value):
        return value is not None and value.strip() != ""
