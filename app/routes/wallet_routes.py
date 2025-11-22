from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from app.models.wallet_model import WalletModel
from app.models.transaction_model import TransactionModel
from app.models.category_model import CategoryModel
from app.utils.validators import Validator
from datetime import datetime

wallet_bp = Blueprint("wallet", __name__, url_prefix="/wallet")


@wallet_bp.before_request
def require_login():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))


@wallet_bp.route("/")
def wallet_home():
    user_id = session["user_id"]

    balance = WalletModel.get_balance(user_id)
    categories = CategoryModel.get_all_categories(user_id)

    now = datetime.now()
    limit = WalletModel.get_monthly_limit(user_id, now.year, now.month)
    print("LIMIT OBJECT:", limit)

    return render_template(
        "wallet.html",
        balance=balance,
        categories=categories,
        year=now.year,
        month=now.month,
        limit=limit
    )


@wallet_bp.route("/deposit", methods=["POST"])
def deposit():
    user_id = session["user_id"]

    data = request.get_json()
    amount = data.get("amount") if data else None

    if not Validator.valid_amount(amount):
        return jsonify({"success": False, "message": "Invalid amount"}), 400

    WalletModel.deposit(user_id, float(amount))

    TransactionModel.add_transaction(
        user_id=user_id,
        amount=float(amount),
        category_id=None,
        merchant="Wallet Deposit",
        type="income"
    )

    new_balance = WalletModel.get_balance(user_id)

    return jsonify({
        "success": True,
        "new_balance": new_balance,
        "history_item": {
            "merchant": "Wallet Deposit",
            "category": "Deposit",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "amount": float(amount),
            "type": "income"
        }
    })


@wallet_bp.route("/withdraw", methods=["POST"])
def withdraw():
    user_id = session["user_id"]

    data = request.get_json()
    amount = data.get("amount") if data else None

    if not Validator.valid_amount(amount):
        return jsonify({"success": False, "message": "Invalid amount"}), 400

    result = WalletModel.withdraw(user_id, float(amount))
    if not result["success"]:
        return jsonify({"success": False, "message": result["message"]}), 400

    TransactionModel.add_transaction(
        user_id=user_id,
        amount=float(amount),
        category_id=None,
        merchant="Wallet Withdrawal",
        type="expense"
    )

    new_balance = WalletModel.get_balance(user_id)

    return jsonify({
        "success": True,
        "new_balance": new_balance,
        "history_item": {
            "merchant": "Wallet Withdrawal",
            "category": "Withdrawal",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "amount": float(amount),
            "type": "expense"
        }
    })


@wallet_bp.route("/set-limit", methods=["POST"])
def set_limit():
    user_id = session["user_id"]
    year = int(request.form.get("year"))
    month = int(request.form.get("month"))
    limit = request.form.get("limit")

    try:
        limit = float(limit)
    except:
        flash("Invalid limit", "error")
        return redirect(url_for("wallet.wallet_home"))

    WalletModel.set_monthly_limit(user_id, year, month, limit)

    flash("Monthly limit updated", "success")
    return redirect(url_for("wallet.wallet_home"))


@wallet_bp.route("/balance")
def get_balance():
    user_id = session["user_id"]
    balance = WalletModel.get_balance(user_id)
    return jsonify({"success": True, "balance": balance})
