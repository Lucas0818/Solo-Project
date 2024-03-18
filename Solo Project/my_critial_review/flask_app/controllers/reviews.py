from flask import render_template, session, redirect, request, flash
from flask_app import app
from flask_app.models.review import Review
from flask_app.models.user import User


@app.route("/review/view/<int:id>")
def view_review(id):
    if "user_id" not in session:
        return redirect("/")
    return render_template("view_review.html", user=User.get_by_id(session["user_id"]), reviews=Review.get_all_by_id(id))

@app.route("/review/delete/<int:id>")
def delete_review(id):
    if "user_id" not in session:
        return redirect("/")
    
    Review.delete(id)
    flash("Review Deleted")
    return redirect("/dashboard")

@app.route("/review/add")
def add_review_form():
    if "user_id" not in session:
        return redirect("/")
    return render_template("add_review.html", user=User.get_by_id(session["user_id"]))

@app.route("/review/add", methods=["POST"])
def add_review():
    if "user_id" not in session:
        return redirect("/")
    if  not Review.validate(request.form):
        return redirect("/review/add")
    Review.add({
        **request.form,
        "user_id": session["user_id"]
    })
    flash("Review added")
    return redirect("/dashboard")

@app.route("/review/edit/<int:id>")
def edit_review_form(id):
    if "user_id" not in session:
        return redirect("/")
    return render_template("edit_review.html", review=Review.get_by_id(id), user=User.get_by_id(session["user_id"]))

@app.route("/review/edit", methods=["POST"])
def edit_review():
    if "user_id" not in session:
        return redirect("/")
    if not Review.validate(request.form):
        return redirect(f"/review/edit/{request.form['id']}")
    
    Review.edit({
        **request.form,
        "user_id": session["user_id"]
        })
    flash("Review updated")
    return redirect(f"/review/view/{request.form['id']}")