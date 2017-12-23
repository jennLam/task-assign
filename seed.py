from sqlalchemy import func
from model import User, Technician, Equipment, Task, Status, Material, TechnicianTask, TaskEquipment, TaskMaterial, connect_to_db, db
from server import app
from datetime import datetime
from update_pkey_seqs import update_pkey_seqs


def load_users():
    """Load users from user_data into database."""

    for line in open("seed_data/user_data"):
        line = line.rstrip()
        user_id, fname, lname, username, email, password, notification = line.split(",")

        user = User(user_id=user_id, fname=fname, lname=lname, username=username,
                    email=email, password=password, notification=notification)

        # We need to add to the session or it won't be stored
        db.session.add(user)

    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()
    load_users()
    update_pkey_seqs()
