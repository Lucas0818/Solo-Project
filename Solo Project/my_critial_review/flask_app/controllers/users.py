from flask import render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.user import User

bcrypt = Bcrypt(app)

@app.route("/user/register", methods=["POST"])
def register():

    if not User.validate_new_user(request.form):
        return redirect("/")
    
    hashed_password = bcrypt.generate_password_hash(request.form["password"])

    user_id = User.create({
        **request.form,
        "password": hashed_password
    })

    session["user_id"] = user_id
    flash("Thank you for registering")
    return redirect("/dashboard")

@app.route("/user/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    user = User.get_by_email(email)

    if not user:
        flash("Invalid Credentials")
        return redirect("/")
    
    if not bcrypt.check_password_hash(user.password, password):
        flash("Invalid Credentials")
        return redirect("/")
    
    session["user_id"] = user.id
    return redirect("/dashboard")

@app.route("/user/logout")
def logout():
    session.clear()
    flash("Have a good day!")
    return redirect("/")