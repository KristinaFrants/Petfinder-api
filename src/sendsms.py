from twilio.rest import Client
import os
from models import Alert, Person

Q = Alert ()

def first_function(number, mess):
    
    account_sid = os.environ.get('SID_KEV') 
    auth_token = os.environ.get('TOKEN_KEV')
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            body=mess,
            from_='+12064660790',
            to=number
        )

    print(message.sid)
    # return repr(Q._queue)