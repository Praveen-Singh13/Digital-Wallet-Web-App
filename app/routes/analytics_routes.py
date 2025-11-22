from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for
from datetime import datetime
from app.models.analytics_model import AnalyticsModel
from app.utils.alerts import AlertEngine

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")

@analytics_bp.before_request
def require_login():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

@analytics_bp.route("/")
def analytics_home():
    user_id = session["user_id"]
    now = datetime.now()

    monthly_summary = AnalyticsModel.get_monthly_summary(user_id, now.year, now.month)
    category_dist = AnalyticsModel.get_category_distribution(user_id, now.year, now.month)
    yearly_totals = AnalyticsModel.get_yearly_totals(user_id, now.year)

    overspend_status = AnalyticsModel.detect_overspending(user_id, now.year, now.month)

    alerts = AlertEngine.generate_analytics_alerts(overspend_status)

    return render_template(
        "analytics.html",
        summary=monthly_summary,
        distribution=category_dist,
        yearly=yearly_totals,
        overspending=overspend_status,
        alerts=alerts
    )

@analytics_bp.route("/data/monthly")
def api_monthly_summary():
    user_id = session["user_id"]
    year = int(request.args.get("year"))
    month = int(request.args.get("month"))

    data = AnalyticsModel.get_monthly_summary(user_id, year, month)
    return jsonify({"success": True, "data": data})

@analytics_bp.route("/data/category")
def api_category_distribution():
    user_id = session["user_id"]
    year = int(request.args.get("year"))
    month = int(request.args.get("month"))

    data = AnalyticsModel.get_category_distribution(user_id, year, month)
    return jsonify({"success": True, "data": data})

@analytics_bp.route("/data/yearly")
def api_yearly_totals():
    user_id = session["user_id"]
    year = int(request.args.get("year"))

    data = AnalyticsModel.get_yearly_totals(user_id, year)
    return jsonify({"success": True, "data": data})

@analytics_bp.route("/alerts")
def api_overspending_alert():
    user_id = session["user_id"]
    year = int(request.args.get("year"))
    month = int(request.args.get("month"))

    status = AnalyticsModel.detect_overspending(user_id, year, month)
    alerts = AlertEngine.generate_analytics_alerts(status)

    return jsonify({"success": True, "alerts": alerts})
