from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from datetime import datetime
from app.models.user_model import UserModel
from app.models.wallet_model import WalletModel
from app.utils.validators import Validator

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")


@profile_bp.before_request
def require_login():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))


@profile_bp.route("/")
def profile_home():
    user_id = session["user_id"]
    user = UserModel.get_user_by_id(user_id)

    now = datetime.now()
    limit = WalletModel.get_monthly_limit(user_id, now.year, now.month)

    return render_template(
        "profile.html",
        user=user,
        limit=limit,
        year=now.year,
        month=now.month
    )


@profile_bp.route("/update", methods=["POST"])
def update_profile():
    user_id = session["user_id"]
    name = request.form.get("name")
    email = request.form.get("email")

    if not Validator.valid_email(email):
        flash("Invalid email format", "error")
        return redirect(url_for("profile.profile_home"))

    UserModel.update_profile(user_id, name, email)
    session["user_name"] = name

    flash("Profile updated successfully", "success")
    return redirect(url_for("profile.profile_home"))


@profile_bp.route("/password", methods=["POST"])
def change_password():
    user_id = session["user_id"]
    old = request.form.get("old_password")
    new = request.form.get("new_password")
    confirm = request.form.get("confirm_password")

    user = UserModel.validate_login(UserModel.get_user_by_id(user_id)["email"], old)
    if not user:
        flash("Incorrect old password", "error")
        return redirect(url_for("profile.profile_home"))

    if new != confirm:
        flash("New passwords do not match", "error")
        return redirect(url_for("profile.profile_home"))

    UserModel.change_password(user_id, new)

    flash("Password updated successfully", "success")
    return redirect(url_for("profile.profile_home"))


@profile_bp.route("/set-limit", methods=["POST"])
def set_monthly_limit():
    user_id = session["user_id"]
    year = int(request.form.get("year"))
    month = int(request.form.get("month"))
    limit = request.form.get("limit")

    try:
        limit = float(limit)
    except:
        flash("Invalid limit amount", "error")
        return redirect(url_for("profile.profile_home"))

    WalletModel.set_monthly_limit(user_id, year, month, limit)

    flash("Monthly spending limit updated", "success")
    return redirect(url_for("profile.profile_home"))
