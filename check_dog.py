'''checks dog against age and size criteria
and sends whatsapp notification in case of new dog'''

import datetime
import re
import os
from twilio.rest import Client
from dotenv import load_dotenv

from connection import DB_SESSION
from models import Doggos

load_dotenv()

ACCOUNT_SID = os.getenv('ACCOUNT_SID')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
MOBILE = os.getenv('MOBILE')

CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)

YEARS = 3 * 365
CUT_OF_AGE = datetime.date.today() - datetime.timedelta(days=YEARS)

def check_doggo(dog_id):
    '''handling the age and size check giving the dog id and sending the message'''
    dog = DB_SESSION.query(Doggos).get(dog_id)
    try:
        age = datetime.datetime.strptime(dog.birthday.strip(), '%d.%m.%Y').date()
    except:
        age = datetime.datetime.strptime(dog.birthday.strip(), '%m/%Y').date()
    else:
        try:
            age = re.search('[0-9]{4}', dog.birthday.strip())
            age = datetime.datetime.strptime(age.group(0), '%Y').date()
        except:
            pass

    if CUT_OF_AGE <= age and dog.size != 'klein' and dog.age_span != 'senior':
        CLIENT.messages.create(
            from_='whatsapp:+14155238886',
            body=f'Es gibt einen neuen Hund im Tierheim. \
             Er heißt {dog.name} und ist ein {dog.breed}',
            to=f'whatsapp:{MOBILE}'
            )
