from twilio.rest import Client
import os


def send_sms(to_number, body_message):

    # Your Account SID from twilio.com/console
    account_sid = os.environ.get("ACCOUNT_SID")
    # Your Auth Token from twilio.com/console
    auth_token = os.environ.get("AUTH_TOKEN")

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=to_number,
        from_=os.environ.get("TWILIO_NUM"),
        body=body_message)

    print message.sid
