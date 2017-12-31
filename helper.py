from model import User, Technician, Equipment, Task, Status, Material, TechnicianTask, TaskEquipment, db
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


# def get_tasks(user_id):
#     """Get tasks."""

#     tasks = Task.query.filter_by(user_id=user_id).all()

#     return tasks


# def get_sidebar_info(user_id):
#     """Get information to populate sidebar."""

#     tasks = get_tasks(user_id)

#     return {"tasks": tasks}
