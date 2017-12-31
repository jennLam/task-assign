from sqlalchemy import func
from model import User, Technician, Equipment, Task, Status
from model import connect_to_db, db
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

        db.session.add(user)

    db.session.commit()


def load_techs():
    """Load technicians from tech_data into database."""

    for line in open("seed_data/tech_data"):
        line = line.rstrip()
        tech_id, user_id, name, email, phone_number, start_date = line.split(",")

        tech = Technician(tech_id=tech_id, user_id=user_id, name=name,
                          email=email, phone_number=phone_number, start_date=start_date)

        db.session.add(tech)

    db.session.commit()


def load_equips():
    """Load equipments from equip_data into database."""

    for line in open("seed_data/equip_data"):
        line = line.rstrip()
        equip_id, user_id, name, ein, eq_type = line.split(",")

        equip = Equipment(equip_id=equip_id, user_id=user_id, name=name,
                          ein=ein, eq_type=eq_type)

        db.session.add(equip)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()
    load_users()
    load_techs()
    load_equips()
    update_pkey_seqs()
