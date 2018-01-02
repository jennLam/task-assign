from flask import Flask, render_template, redirect, request, flash, session, g, url_for
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from model import User, Technician, Equipment, Task, Status, Assignment, AssignmentTask, AssignmentTechnician, AssignmentEquipment, AssignStatus
from model import connect_to_db, db
from functools import wraps
import os
from helper import check_and_add, add_to_database


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
        return render_template("home.html", user=g.current_user)

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

            return redirect("/")
        else:
            flash("Incorrect password.")
    else:
        flash("User does not exist.")

    return redirect(request.referrer)


@app.route("/resources")
@login_required
def manage_resources():
    """Show resources page."""

    return render_template("resources.html")


@app.route("/assign")
@login_required
def show_assign():
    """Show assignments page."""

    completed_stat = AssignStatus.query.filter_by(name="Completed").first()
    ip_stat = AssignStatus.query.filter_by(name="In Progress").first()
    tbd_stat = AssignStatus.query.filter_by(name="To Be Done").first()

    completed = Assignment.query.filter_by(user_id=g.user_id,
                                           assignstat_id=completed_stat.assignstat_id).all()

    ip = Assignment.query.filter_by(user_id=g.user_id,
                                    assignstat_id=ip_stat.assignstat_id).all()

    tbd = Assignment.query.filter_by(user_id=g.user_id,
                                     assignstat_id=tbd_stat.assignstat_id).all()

    return render_template("assign.html", completed=completed, ip=ip, tbd=tbd)


@app.route("/show-assign-form")
@login_required
def show_assign_form():
    """Show assignment form."""

    return render_template("assign-form.html")


@app.route("/add-assign", methods=["POST"])
@login_required
def add_assign():
    """Add assignment to database."""

    task = request.form.get("task")
    tech = request.form.get("tech")
    equip = request.form.get("equip")
    details = request.form.get("details")

    if task and tech and equip:
        print task, tech, equip

        task_ob = Task.query.get(task)
        equip_ob = Equipment.query.get(equip)

        name = task_ob.name + " (" + equip_ob.name + ")"
        tbd_stat = AssignStatus.query.filter_by(name="To Be Done").first()

        new_assign = Assignment(user_id=g.user_id, assignstat_id=tbd_stat.assignstat_id,
                                name=name, details=details)

        add_to_database(new_assign)

        new_assigntask = AssignmentTask(task_id=task, assignment_id=new_assign.assignment_id)

        new_assigntech = AssignmentTechnician(tech_id=tech, assignment_id=new_assign.assignment_id)

        new_assignequip = AssignmentEquipment(equip_id=equip, assignment_id=new_assign.assignment_id)

        add_to_database(new_assigntask)
        add_to_database(new_assigntech)
        add_to_database(new_assignequip)

        flash("Assignment successfully created.", "success")

    else:
        flash("Make sure you have enough resources before creating a new assignment.", "warning")

    return redirect(request.referrer)


@app.route("/show-task-form")
@login_required
def show_task_form():
    """Show task form."""

    return render_template("task-form.html")


@app.route("/add-task", methods=["POST"])
@login_required
def add_task():
    """Add task to database."""

    task = request.form.get("task")
    details = request.form.get("details")

    print task, details

    existing_task = Task.query.filter_by(user_id=g.user_id, name=task).first()

    new_task = Task(user_id=g.user_id, name=task, details=details)

    check_and_add(existing_task, new_task)

    return redirect(request.referrer)


@app.route("/show-tech-form")
@login_required
def show_tech_form():
    """Show technician form."""

    return render_template("tech-form.html")


@app.route("/add-tech", methods=["POST"])
@login_required
def add_tech():
    """Add technician to database."""

    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    start = request.form.get("start")

    existing_tech = Technician.query.filter_by(name=name).first()

    new_tech = Technician(user_id=g.user_id, name=name, email=email,
                          phone_number=phone, start_date=start)

    check_and_add(existing_tech, new_tech)

    return redirect(request.referrer)


@app.route("/show-equip-form")
@login_required
def show_equip_form():
    """Show equipment form."""

    return render_template("equip-form.html")


@app.route("/add-equip", methods=["POST"])
@login_required
def add_equip():
    """Add equipment to database."""

    name = request.form.get("name")
    ein = request.form.get("ein")
    eq_type = request.form.get("type")

    existing_equip = Equipment.query.filter_by(name=name).first()

    new_equip = Equipment(user_id=g.user_id, name=name, ein=ein, eq_type=eq_type)

    check_and_add(existing_equip, new_equip)

    return redirect(request.referrer)


@app.route("/show-status-form")
@login_required
def show_status_form():
    """Show status form."""

    return render_template("status-form.html")


@app.route("/add-status", methods=["POST"])
@login_required
def add_status():
    """Add status to database."""

    status = request.form.get("status")

    existing_status = Status.query.filter_by(name=status).first()

    new_status = Status(user_id=g.user_id, name=status)

    check_and_add(existing_status, new_status)

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
