from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.user_model import UserModel
from app.utils.validators import Validator
from app.config.database import get_db_connection

auth_bp = Blueprint("auth", __name__,)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        if not Validator.valid_email(email):
            flash("Invalid email format", "error")
            return redirect(url_for("auth.login"))

        user = UserModel.validate_login(email, password)
        if user:
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            return redirect(url_for("wallet.wallet_home"))
        else:
            flash("Incorrect email or password", "error")

    return render_template("login.html")


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if not Validator.valid_email(email):
            flash("Invalid email format", "error")
            return redirect(url_for("auth.signup"))

        if password != confirm:
            flash("Passwords do not match", "error")
            return redirect(url_for("auth.signup"))

        result = UserModel.create_user(name, email, password)

        if result["created"]:
            user_id = result["user_id"]

            default_categories = [
                ("Food", "expense"),
                ("Travel", "expense"),
                ("Shopping", "expense"),
                ("Utilities", "expense"),
                ("Bills", "expense"),
                ("Entertainment", "expense"),
                ("Healthcare", "expense"),
                ("Other", "expense"),
                ("Salary", "income"),
                ("Bonus", "income")
            ]

            conn = get_db_connection()
            cur = conn.cursor()

            cur.executemany(
                "INSERT INTO categories (name, type, user_id) VALUES (?, ?, ?)",
                [(name, ctype, user_id) for name, ctype in default_categories]
            )

            conn.commit()

            # Initialize wallet for the new user
            conn.execute("INSERT INTO wallet (user_id, balance) VALUES (?, ?)", (user_id, 0))
            conn.commit()

            # -----------------------------
            flash("Account created successfully. Please login.", "success")
            return redirect(url_for("auth.login"))

        else:
            flash(result["message"], "error")

    return render_template("signup.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
