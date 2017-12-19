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
    phone_number = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)

    user = db.relationship("User", backref=db.backref("technicians"))

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

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<Equipment equip_id=%s user_id=%s status_id=%s name=%s ein=%s eq_type=%s>"
        return s % (self.equip_id, self.user_id, self.status_id, self.name, self.ein, self.eq_type)


class Task(db.Model):
    """Task model."""

    __tablename__ = "tasks"

    task_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    status_id = db.Column(db.Integer, db.ForeignKey("statuses.status_id"))
    name = db.Column(db.String(25), nullable=False)
    details = db.Column(db.String(500), nullable=False)

    user = db.relationship("User", backref=db.backref("tasks"))
    status = db.relationship("Status", backref=db.backref("tasks"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<Task task_id=%s user_id=%s status_id=%s name=%s details=%s>"
        return s % (self.task_id, self.user_id, self.status_id, self.name, self.details)


class Status(db.Model):
    """Status model."""

    __tablename__ = "statuses"

    status_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<Status status_id=%s name=%s>"
        return s % (self.status_id, self.name)


class Material(db.Model):
    """Material model."""

    __tablename__ = "materials"

    material_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    name = db.Column(db.String(25), nullable=False)
    details = db.Column(db.String(500), nullable=False)

    user = db.relationship("User", backref=db.backref("tasks"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<Task material_id=%s user_id=%s name=%s details=%s>"
        return s % (self.material_id, self.user_id, self.name, self.details)


class TechnicianTask(db.Model):
    """TechnicianTask model."""

    __tablename__ = "techniciantasks"

    techtask_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    tech_id = db.Column(db.Integer, db.ForeignKey("technicians.tech_id"))
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.task_id"))

    technician = db.relationship("Technician", backref=db.backref("techniciantasks"))
    task = db.relationship("Task", backref=db.backref("techniciantasks"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<TechnicianTask techtask_id=%s tech_id=%s task_id=%s>"
        return s % (self.techtask_id, self.tech_id, self.task_id)


class TaskEquipment(db.Model):
    """TaskEquipment model."""

    __tablename__ = "taskequipments"

    taskequip_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    equip_id = db.Column(db.Integer, db.ForeignKey("equipments.equip_id"))
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.task_id"))

    equipment = db.relationship("Equipment", backref=db.backref("taskequipments"))
    task = db.relationship("Task", backref=db.backref("taskequipments"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<TaskEquipment taskequip_id=%s equip_id=%s task_id=%s>"
        return s % (self.taskequip_id, self.equip_id, self.task_id)


class TaskMaterial(db.Model):
    """TaskMaterial model."""

    __tablename__ = "taskmaterials"

    taskmaterial_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey("materials.material_id"))
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.task_id"))

    material = db.relationship("Material", backref=db.backref("taskmaterials"))
    task = db.relationship("Task", backref=db.backref("taskmaterials"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<TaskMaterial taskmaterial_id=%s material_id=%s task_id=%s>"
        return s % (self.taskmaterial_id, self.material_id, self.task_id)


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
