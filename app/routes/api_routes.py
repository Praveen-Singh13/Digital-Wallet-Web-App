from flask import Blueprint, request, jsonify, session
from app.models.wallet_model import WalletModel
from app.models.transaction_model import TransactionModel
from app.models.category_model import CategoryModel
from app.models.analytics_model import AnalyticsModel

api_bp = Blueprint("api", __name__, url_prefix="/api")


def auth_required():
    if "user_id" not in session:
        return False, jsonify({"success": False, "message": "Unauthorized"}), 401
    return True, None, None


@api_bp.route("/wallet/balance")
def get_balance():
    ok, resp, code = auth_required()
    if not ok:
        return resp, code

    user_id = session["user_id"]
    balance = WalletModel.get_balance(user_id)

    return jsonify({"success": True, "balance": balance})


@api_bp.route("/wallet/deposit", methods=["POST"])
def deposit():
    ok, resp, code = auth_required()
    if not ok:
        return resp, code

    user_id = session["user_id"]
    data = request.json

    try:
        amount = float(data.get("amount", 0))
    except:
        return jsonify({"success": False, "message": "Invalid amount"}), 400

    WalletModel.deposit(user_id, amount)

    return jsonify({"success": True, "balance": WalletModel.get_balance(user_id)})


@api_bp.route("/wallet/withdraw", methods=["POST"])
def withdraw():
    ok, resp, code = auth_required()
    if not ok:
        return resp, code

    user_id = session["user_id"]
    data = request.json

    try:
        amount = float(data.get("amount", 0))
    except:
        return jsonify({"success": False, "message": "Invalid amount"}), 400

    result = WalletModel.withdraw(user_id, amount)

    if not result["success"]:
        return jsonify(result), 400

    return jsonify({"success": True, "balance": WalletModel.get_balance(user_id)})


@api_bp.route("/transactions/add", methods=["POST"])
def add_transaction():
    ok, resp, code = auth_required()
    if not ok:
        return resp, code

    data = request.json
    user_id = session["user_id"]

    TransactionModel.add_transaction(
        user_id=user_id,
        amount=data.get("amount"),
        category_id=data.get("category_id"),
        merchant=data.get("merchant"),
        type=data.get("type")
    )

    return jsonify({"success": True})


@api_bp.route("/transactions/all")
def get_all_transactions():
    ok, resp, code = auth_required()
    if not ok:
        return resp, code

    user_id = session["user_id"]
    transactions = TransactionModel.get_all_transactions(user_id)

    return jsonify({"success": True, "transactions": transactions})


@api_bp.route("/categories")
def categories():
    ok, resp, code = auth_required()
    if not ok:
        return resp, code

    user_id = session["user_id"]
    cats = CategoryModel.get_all_categories(user_id)

    return jsonify({"success": True, "categories": cats})


@api_bp.route("/analytics/monthly")
def analytics_monthly():
    ok, resp, code = auth_required()
    if not ok:
        return resp, code

    user_id = session["user_id"]
    year = int(request.args.get("year"))
    month = int(request.args.get("month"))

    data = AnalyticsModel.get_monthly_summary(user_id, year, month)
    return jsonify({"success": True, "data": data})


@api_bp.route("/analytics/yearly")
def analytics_yearly():
    ok, resp, code = auth_required()
    if not ok:
        return resp, code

    user_id = session["user_id"]
    year = int(request.args.get("year"))

    data = AnalyticsModel.get_yearly_totals(user_id, year)
    return jsonify({"success": True, "data": data})


@api_bp.route("/analytics/category")
def analytics_category():
    ok, resp, code = auth_required()
    if not ok:
        return resp, code

    user_id = session["user_id"]
    year = int(request.args.get("year"))
    month = int(request.args.get("month"))

    data = AnalyticsModel.get_category_distribution(user_id, year, month)
    return jsonify({"success": True, "data": data})
