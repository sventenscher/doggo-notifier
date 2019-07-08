'''checks dog against age and size criteria
and sends whatsapp notification in case of new dog'''

import datetime
import re
import os
from dotenv import load_dotenv
from connection import DB_SESSION
from models import Doggos
import requests

load_dotenv()

BOT_TOKEN = os.getenv('bot_token')
BOT_CHAT_ID = os.getenv('bot_chat_ID')


YEARS = 3 * 365
CUT_OF_AGE = datetime.date.today() - datetime.timedelta(days=YEARS)

def bot_sendtext(dog):

    message = f'''Es gibt einen neuen Hund im Tierheim. \n
Sein Name ist *{dog.name}* und er ist ein *{dog.breed}*. \n
Schau ihn dir hier an: {dog.link}'''

    send_text = f'''https://api.telegram.org/bot{BOT_TOKEN}/SendMessage?chat_id={BOT_CHAT_ID}&parse_mode=Markdown&text={message}'''
    requests.get(send_text)


def bot_sendphoto(dog):

    message = f'''Es gibt einen neuen Hund im Tierheim. Sein Name ist *{dog.name}* und er ist ein *{dog.breed}*. \n
Schau ihn dir hier an: {dog.link}'''
    
    photo_url = re.sub('-150x150','',dog.featured_image_link)
    send_text = f'''https://api.telegram.org/bot{BOT_TOKEN}/SendPhoto?chat_id={BOT_CHAT_ID}&photo={photo_url}&parse_mode=Markdown&caption={message}'''
    requests.get(send_text)

def check_doggo(dog_id):
    '''handling the age and size check giving the dog id and sending the message'''
    
    dog = DB_SESSION.query(Doggos).get(dog_id)

    try:
        age = datetime.datetime.strptime(dog.birthday.strip(), '%d.%m.%Y').date()
    except ValueError:
        age = re.search('[0-9]{2}/[0-9]{4}', dog.birthday.strip())
        age = datetime.datetime.strptime(age.group(0), '%m/%Y').date()
    else:
        try:
            age = re.search('[0-9]{4}', dog.birthday.strip())
            age = datetime.datetime.strptime(age.group(0), '%Y').date()
        except ValueError:
            pass

    if CUT_OF_AGE <= age and dog.size != 'klein' and dog.age_span != 'senior':
        bot_sendphoto(dog)
