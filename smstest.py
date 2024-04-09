# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
import config


# auth credentials
account_sid = config.TWILIO_ACCOUNT_SID
auth_token = config.TWILIO_AUTH_TOKEN

client = Client(account_sid, auth_token)


def send_sms():
    # global client
    message = client.messages.create(
        body='Your Account is loggedIn' ,
        from_='+18329796131',
        to='+918110949621'
    )
    return message.sid


print(send_sms())