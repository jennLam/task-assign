from sqlalchemy import func
from model import User, Technician, Equipment, Task, Status, AssignStatus
from model import connect_to_db, db
from server import app, bcrypt
from datetime import datetime
from update_pkey_seqs import update_pkey_seqs


def load_users():
    """Load users from user_data into database."""

    for line in open("seed_data/user_data"):
        line = line.rstrip()
        user_id, fname, lname, username, email, password = line.split(",")

        hashed_pw = bcrypt.generate_password_hash(password)

        user = User(user_id=user_id, fname=fname, lname=lname, username=username,
                    email=email, password=hashed_pw)

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


def load_assignstats():
    """Load assignment statuses from assignstat_data into database."""

    for line in open("seed_data/assignstat_data"):
        line = line.rstrip()
        assignstat = AssignStatus(name=line)

        db.session.add(assignstat)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()
    load_users()
    load_techs()
    load_equips()
    load_assignstats()
    update_pkey_seqs()
