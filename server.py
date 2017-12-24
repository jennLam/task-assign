from flask import Flask, render_template, redirect, request, flash, session, g, url_for
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from model import User, Technician, Equipment, Task, Status, Material, TechnicianTask, TaskEquipment, TaskMaterial, connect_to_db, db
from functools import wraps
import os

app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY")

app.jinja_env.undefined = StrictUndefined


@app.before_request
def before_request():
    """Run before each route."""

    g.user_id = session.get("user_id")
    if g.user_id:
        g.current_user = User.query.get(g.user_id)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if g.user_id:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('show_login_form'))

    return wrap


@app.route("/")
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route("/register")
def show_register_form():

    return render_template("register.html")


@app.route("/register", methods=["POST"])
def process_register_info():
    """Get registration form information."""

    # Get information from registration from
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    uname = request.form.get("uname")
    email = request.form.get("email")
    password = request.form.get("password")
    notification = request.form.get("notification")

    # Get existing user in database
    existing_user = User.query.filter_by(username=uname).first()

    # Make new user
    new_user = User(fname=fname, lname=lname, username=uname, email=email,
                    password=password, notification=notification)

    # Check database, add to database
    check_and_add(existing_user, new_user)

    return redirect("/")


@app.route("/login", methods=["POST"])
def process_login():
    """Process login."""

    username = request.form.get("username")
    password = request.form.get("password")

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        if existing_user.password == password:
            session["user_id"] = existing_user.user_id
            session["user_name"] = existing_user.fname

            return redirect("/user/" + str(session["user_id"]))
        else:
            flash("Incorrect password.")
    else:
        flash("User does not exist.")

    return redirect(request.referrer)


@app.route("/user/<user_id>")
@login_required
def show_user_page(user_id):
    """Show user's homepage."""

    return render_template("home.html", user=g.current_user)


if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # DebugToolbarExtension(app)

    app.run(port=5000, host="0.0.0.0")
