from flask import Flask, redirect, url_for, g
import sqlite3
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent


def create_app():
    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "templates"),
        static_folder=str(BASE_DIR / "static")
    )
    from app.config.config import Config
    app.config.from_object(Config)

    from app.config.database import init_db_if_needed
    init_db_if_needed()

    @app.context_processor
    def inject_now():
        return {"now": datetime.utcnow}

    @app.teardown_appcontext
    def close_db(exception):
        conn = g.pop("db", None)
        if conn:
            conn.close()

    from app.routes.auth_routes import auth_bp
    from app.routes.wallet_routes import wallet_bp
    from app.routes.transaction_routes import transaction_bp
    from app.routes.analytics_routes import analytics_bp
    from app.routes.profile_routes import profile_bp
    from app.routes.api_routes import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(wallet_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(api_bp)

    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))

    return app
