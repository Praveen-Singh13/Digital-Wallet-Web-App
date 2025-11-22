from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from app.models.transaction_model import TransactionModel
from app.models.category_model import CategoryModel
from app.models.wallet_model import WalletModel
from app.utils.validators import Validator
from datetime import datetime

transaction_bp = Blueprint("transactions", __name__, url_prefix="/transactions")


@transaction_bp.before_request
def require_login():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))


@transaction_bp.route("/")
def transactions_home():
    user_id = session["user_id"]

    transactions = TransactionModel.get_all_transactions(user_id)
    categories = CategoryModel.get_all_categories(user_id)

    print("CATEGORIES:", categories)

    return render_template(
        "transactions.html",
        transactions=transactions,
        categories=categories
    )


@transaction_bp.route("/add", methods=["GET", "POST"])
def add_transaction():
    user_id = session["user_id"]

    if request.method == "POST":
        amount = request.form.get("amount")
        merchant = request.form.get("merchant")
        category_id = request.form.get("category_id")
        t_type = request.form.get("type")

        if not Validator.valid_amount(amount):
            flash("Invalid amount", "error")
            return redirect(url_for("transactions.add_transaction"))

        TransactionModel.add_transaction(
            user_id,
            float(amount),
            category_id,
            merchant,
            t_type
        )

        if t_type == "expense":
            WalletModel.withdraw(user_id, float(amount))
        else:
            WalletModel.deposit(user_id, float(amount))

        flash("Transaction added successfully", "success")
        return redirect(url_for("transactions.transactions_home"))

    categories = CategoryModel.get_all_categories(user_id)
    return render_template("transaction_add.html", categories=categories)


@transaction_bp.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    user_id = session["user_id"]
    txn = TransactionModel.get_transaction_by_id(transaction_id, user_id)

    if not txn:
        flash("Transaction not found", "error")
        return redirect(url_for("transactions.transactions_home"))

    if request.method == "POST":
        amount = request.form.get("amount")
        merchant = request.form.get("merchant")
        category_id = request.form.get("category_id")
        t_type = request.form.get("type")

        if not Validator.valid_amount(amount):
            flash("Invalid amount", "error")
            return redirect(url_for("transactions.edit_transaction", transaction_id=transaction_id))

        TransactionModel.edit_transaction(
            transaction_id,
            user_id,
            float(amount),
            category_id,
            merchant,
            t_type
        )

        flash("Transaction updated", "success")
        return redirect(url_for("transactions.transactions_home"))

    categories = CategoryModel.get_all_categories(user_id)

    return render_template(
        "transaction_add.html",
        edit=True,
        transaction=txn,
        categories=categories
    )


@transaction_bp.route("/delete/<int:transaction_id>", methods=["POST"])
def delete_transaction(transaction_id):
    user_id = session["user_id"]

    txn = TransactionModel.get_transaction_by_id(transaction_id, user_id)
    if not txn:
        return jsonify({"success": False, "message": "Not found"}), 404

    TransactionModel.delete_transaction(transaction_id, user_id)

    return jsonify({"success": True, "message": "Deleted"})


@transaction_bp.route("/filter", methods=["GET"])
def filter_transactions():
    user_id = session["user_id"]

    category_id = request.args.get("category")
    month = request.args.get("month")
    year = request.args.get("year")
    merchant = request.args.get("merchant")

    category_id = int(category_id) if category_id else None
    month = int(month) if month else None
    year = int(year) if year else None

    filtered = TransactionModel.filter_transactions(
        user_id=user_id,
        category_id=category_id,
        month=month,
        year=year,
        merchant=merchant
    )

    return jsonify({"success": True, "transactions": filtered})
