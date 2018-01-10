# Task Assign

Task Assign is a web application to help manufacturing leads assign daily tasks to their team. You can add resources, create assigments and send texts with assignment details to  technicians. Technicians can reply to texts to update assignment statuses.


# Screenshots

![alt text]("/static/taskassignhome.png" "Task Assign")
This is main page.

![alt text]("/static/taskassignadd.png" "Add Resources")
This is the user's homepage. The user can add resources and create assignments.

![alt text]("/static/taskassigndetails.png" "Assignment Details")
Click on an assignment to see all the details.

![alt text]("/static/phone.png" "Texts")
Press the send text button to send assignment details to the technician. The technician can reply to the text to update the assignment status.

### Tech

Task Assign is created with the following:

Python, PostgreSQL, SQLAlchemy, Flask, Jinja, Javascript, JQuery, Boostrap, Chart.js, Twilio API


### Set-Up
You will need:
- Twilio Account

Create and launch a virtual environment
```sh
$ virtualenv env
$ source env/bin/activate
```
Install requirements
```sh
$ pip install -r requirements.txt
```
Input your keys in a file called secrets.sh
```sh
export FLASK_SECRET_KEY="flask_secret_key here"
export ACCOUNT_SID="Twilio account_sid here"
export AUTH_TOKEN="Twilio auth_token here"
export TWILIO_NUM="Twilio number here"
```

Source your file into the environment
```sh
$ source secrets.sh
```
Launch server
```sh
$ python server.py
```
Navigate to server address.
```sh
localhost:5000
```
