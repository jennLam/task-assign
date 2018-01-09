from model import db, User, Technician, Equipment, Task, Status
from flask import flash


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