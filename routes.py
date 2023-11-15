from flask import Blueprint, redirect, render_template, session
from init import db
from models import Feedback, User
from forms import FeedbackForm, LoginForm, UserForm


app_routes = Blueprint("app_routes", __name__, template_folder="templates")


@app_routes.route("/")
def home():
    if session.get("user_id", None):
        return redirect(f"/users/{session['user_id']}")
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
    return redirect("/register")

@app_routes.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id")
    return redirect("/")

@app_routes.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    user = db.get_or_404(User, username)
    if user and session["user_id"] == user.username:
        db.session.delete(user)
        db.session.commit()
    return redirect('/')

@app_routes.route("/users/<username>/add", methods=["GET", "POST"])
def add_feedback(username):
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback()
        form.populate_obj(feedback)
        feedback.username=username
        db.session.add(feedback)
        db.session.commit()
        return redirect("/")
    return render_template("feedback_form.html", form=form)

@app_routes.route("/feedback/<feedback_id>/update", methods=["GET","POST"])
def edit_feedback(feedback_id):
    feedback = db.get_or_404(Feedback, feedback_id)
    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit() and session["user_id"] == feedback.username:
        form.populate_obj(feedback)
        db.session.add(feedback)
        db.session.commit()
        return redirect(f"/users/{session['user_id']}")
    return render_template("feedback_form.html", form=form)

@app_routes.route("/feedback/<feedback_id>/delete", methods=['POST'])
def delete_feedback(feedback_id):
    feedback = db.get_or_404(Feedback, feedback_id)
    if feedback and session["user_id"] == feedback.username:
        db.session.delete(feedback)
        db.session.commit()
    return redirect(f"/users/{session['user_id']}")
    
