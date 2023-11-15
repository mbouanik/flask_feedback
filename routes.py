from flask import Blueprint, flash, redirect, render_template, session
from init import db
from models import User
from forms import LoginForm, UserForm


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
        return redirect(f"/users/{new_user.username}")
    return render_template("sign_up.html", form=form)

@app_routes.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if User.authenticate(username, password):
            session["user_id"] = username
            return redirect(f"/users/{username}")
    return render_template("login.html", form=form)

@app_routes.route("/users/<username>")
def secret(username):
    if session.get("user_id", None):
        user = db.get_or_404(User, username)
        return render_template("secret.html", user=user)
    flash("Login first")
    return redirect("/register")

@app_routes.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id")
    return redirect("/")
