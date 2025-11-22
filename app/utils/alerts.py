class AlertEngine:

    @staticmethod
    def generate_analytics_alerts(overspend_status):
        alerts = []

        if not overspend_status.get("limit_set"):
            alerts.append({
                "type": "info",
                "message": "No monthly spending limit set. Set one to track overspending."
            })
            return alerts

        limit = overspend_status.get("limit", 0)
        spent = overspend_status.get("spent", 0)
        exceeded = overspend_status.get("exceeded", False)

        if exceeded:
            alerts.append({
                "type": "danger",
                "message": f"You exceeded your monthly limit of ₹{limit:.2f} by spending ₹{spent:.2f}!"
            })
        else:
            percentage = (spent / limit * 100) if limit > 0 else 0

            if percentage >= 90:
                alerts.append({
                    "type": "warning",
                    "message": f"You're close to exceeding your monthly limit. You've used {percentage:.1f}% of your budget."
                })
            elif percentage >= 60:
                alerts.append({
                    "type": "info",
                    "message": f"You're spending steadily. {percentage:.1f}% of your monthly limit used."
                })

        return alerts


class RuleBasedAlertEngine:

    @staticmethod
    def analyze_transaction(amount, category_name, monthly_limit=None, spent_so_far=None):
        alerts = []

        if amount > 10000:
            alerts.append({
                "type": "warning",
                "message": f"High-value transaction detected: ₹{amount:.2f} in {category_name}"
            })

        if monthly_limit is not None and spent_so_far is not None:
            projected = spent_so_far + amount
            if projected > monthly_limit:
                alerts.append({
                    "type": "danger",
                    "message": "This transaction will exceed your monthly spending limit!"
                })

        return alerts
