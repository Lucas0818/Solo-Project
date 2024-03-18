from flask import render_template, session, redirect
from flask_app import app
from flask_app.models.user import User
from flask_app.models.review import Review

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return("/")
    return render_template("dashboard.html", user=User.get_by_id(session["user_id"]), reviews=Review.get_all())