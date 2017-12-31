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

    if g.user_id:
        return redirect("/user/" + str(g.user_id))

    return render_template("homepage.html")


@app.route("/register")
def show_register_form():

    return render_template("register.html")


def add_to_database(item):
    """Add item to the database."""

    db.session.add(item)
    db.session.commit()


def check_and_add(existing_item, item):
    """Check if an item already exists in the database and adds it if it doesn't."""

    # Check if it exists
    if existing_item:
        flash(item.__class__.__name__ + " already exists.", "danger")
        return
    # If not, add to database
    else:
        add_to_database(item)
        flash(item.__class__.__name__ + " successfully added.", "success")


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

    if user_id == str(g.user_id):
        return render_template("home.html", user=g.current_user)
    else:
        flash("Incorrect user.", "warning")
        return redirect("/user/" + str(session["user_id"]))


@app.route("/show-task-form")
def show_task_form():
    """Show task form."""

    return render_template("task.html")


@app.route("/add-task", methods=["POST"])
def add_task():
    """Add task to database."""

    task = request.form.get("task")
    details = request.form.get("details")

    print task, details

    existing_task = Task.query.filter_by(name=task).first()

    new_task = Task(name=task, details=details)

    check_and_add(existing_task, new_task)

    return redirect(request.referrer)


@app.route("/show-tech-form")
def show_tech_form():
    """Show technician form."""

    return render_template("tech.html")


@app.route("/add-tech", methods=["POST"])
def add_tech():
    """Add technician to database."""

    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    start = request.form.get("start")

    existing_tech = Technician.query.filter_by(name=name).first()

    new_tech = Technician(name=name, email=email, phone_number=phone, start_date=start)

    check_and_add(existing_tech, new_tech)

    return redirect(request.referrer)


@app.route("/logout")
@login_required
def process_logout():
    """Process logout."""

    session.clear()

    return redirect("/")


if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # DebugToolbarExtension(app)

    app.run(port=5000, host="0.0.0.0")
