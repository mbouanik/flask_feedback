from flask import Blueprint, redirect, render_template, session
from init import db
from models import User
from forms import UserForm


app_routes = Blueprint("app_routes", __name__, template_folder="templates")


@app_routes.route("/")
def home():
    return redirect("/register") 

@app_routes.route("/register", methods=["GET", "POST"])
def sign_up():
    form = UserForm()
    if form.validate_on_submit():
        new_user = User.registration(
            username=form.username.data,
            pwd=form.password.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        db.session.add(new_user)
        db.session.commit()
        session["user_id"] = new_user.username
    return render_template("sign_up.htnl", form=form)
