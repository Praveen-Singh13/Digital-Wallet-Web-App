from datetime import datetime

class Formatters:

    @staticmethod
    def currency(amount):
        try:
            return f"₹{float(amount):,.2f}"
        except:
            return "₹0.00"

    @staticmethod
    def date(dt_string):
        try:
            dt = datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
            return dt.strftime("%d %b %Y, %I:%M %p")
        except:
            return dt_string

    @staticmethod
    def sql_row_to_dict(row):
        return {key: row[key] for key in row.keys()} if row else {}
