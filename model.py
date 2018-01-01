from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()


class User(db.Model):
    """User model."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    notification = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<User user_id=%s fname=%s lname=%s username=%s email=%s password=%s notification=%s>"
        return s % (self.user_id, self.fname, self.lname, self.username,
                    self.email, self.password, self.notification)


class Technician(db.Model):
    """Technician model."""

    __tablename__ = "technicians"

    tech_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(25), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)

    user = db.relationship("User", backref=db.backref("technicians"))
    assignment = db.relationship("Assignment", secondary="assigntechs", backref="technicians")

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<Technician tech_id=%s user_id=%s name=%s email=%s phone_number=%s start_date=%s>"
        return s % (self.tech_id, self.user_id, self.name, self.email, self.phone_number, self.start_date)


class Equipment(db.Model):
    """Equipment model."""

    __tablename__ = "equipments"

    equip_id = db.Column(db.Integer, autoincrement=True,  nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    status_id = db.Column(db.Integer, db.ForeignKey("statuses.status_id"))
    name = db.Column(db.String(25), nullable=False)
    ein = db.Column(db.Integer, nullable=False)
    eq_type = db.Column(db.String(25), nullable=False)

    user = db.relationship("User", backref=db.backref("equipments"))
    status = db.relationship("Status", backref=db.backref("equipments"))
    assignment = db.relationship("Assignment", secondary="assignequips", backref="equipments")

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<Equipment equip_id=%s user_id=%s status_id=%s name=%s ein=%s eq_type=%s>"
        return s % (self.equip_id, self.user_id, self.status_id, self.name, self.ein, self.eq_type)


#remove status as foreign key to task
class Task(db.Model):
    """Task model."""

    __tablename__ = "tasks"

    task_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    name = db.Column(db.String(25), nullable=False)
    details = db.Column(db.String(500), nullable=False)

    user = db.relationship("User", backref=db.backref("tasks"))
    assignment = db.relationship("Assignment", secondary="assigntasks", backref="tasks")

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<Task task_id=%s user_id=%s name=%s details=%s>"
        return s % (self.task_id, self.user_id, self.name, self.details)


class Status(db.Model):
    """Status model."""

    __tablename__ = "statuses"

    status_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    name = db.Column(db.String(50), nullable=False)

    user = db.relationship("User", backref=db.backref("statuses"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<Status status_id=%s name=%s>"
        return s % (self.status_id, self.name)


class AssignStatus(db.Model):
    """AssignStatus model."""

    __tablename__ = "assignstats"

    assignstat_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<AssignStatus assignstat_id=%s name=%s>"
        return s % (self.assignstat_id, self.name)


#class probably unnecessary, remove material, add all materials in task description
#keep for future when more complex
class Material(db.Model):
    """Material model."""

    __tablename__ = "materials"

    material_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    name = db.Column(db.String(25), nullable=False)
    details = db.Column(db.String(500), nullable=False)

    user = db.relationship("User", backref=db.backref("materials"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<Task material_id=%s user_id=%s name=%s details=%s>"
        return s % (self.material_id, self.user_id, self.name, self.details)


class Assignment(db.Model):
    """Assignment model."""

    __tablename__ = "assignments"

    assignment_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    assignstat_id = db.Column(db.Integer, db.ForeignKey("assignstats.assignstat_id"))
    name = db.Column(db.String(25), nullable=False)
    details = db.Column(db.String(500))

    user = db.relationship("User", backref=db.backref("assignments"))
    assignstat = db.relationship("AssignStatus", backref=db.backref("assignments"))


    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<Assignment assignment_id=%s user_id=%s assignstat_id=%s name=%s details=%s>"
        return s % (self.assignment_id, self.user_id, self.assignstat_id, self.name, self.details)


class AssignmentTechnician(db.Model):
    """AssignmentTechnician model."""

    __tablename__ = "assigntechs"

    assigntech_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    tech_id = db.Column(db.Integer, db.ForeignKey("technicians.tech_id"))
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignments.assignment_id"))

    technician = db.relationship("Technician", backref=db.backref("assigntechs"))
    assignment = db.relationship("Assignment", backref=db.backref("assigntechs"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<AssignmentTechnician assigntech_id=%s tech_id=%s assignment_id=%s>"
        return s % (self.assigntech_id, self.tech_id, self.assignment_id)


class AssignmentEquipment(db.Model):
    """AssignmentEquipment model."""

    __tablename__ = "assignequips"

    assignequip_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    equip_id = db.Column(db.Integer, db.ForeignKey("equipments.equip_id"))
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignments.assignment_id"))

    equipment = db.relationship("Equipment", backref=db.backref("assignequips"))
    assignment = db.relationship("Assignment", backref=db.backref("assignequips"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<AssignmentEquipment assignequip_id=%s equip_id=%s assignment_id=%s>"
        return s % (self.assignequip_id, self.equip_id, self.assignment_id)


class AssignmentTask(db.Model):
    """AssignmentTask model."""

    __tablename__ = "assigntasks"

    assigntask_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.task_id"))
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignments.assignment_id"))

    task = db.relationship("Task", backref=db.backref("assigntasks"))
    assignment = db.relationship("Assignment", backref=db.backref("assigntasks"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<AssignmentTask assigntask_id=%s task_id=%s assignment_id=%s>"
        return s % (self.assigntask_id, self.task_id, self.assignment_id)


def init_app():

    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app, db_uri="postgres:///tasks"):
    """Connect the database to our Flask app."""

    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":

    init_app()
