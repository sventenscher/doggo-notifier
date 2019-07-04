'''checks dog against age and size criteria
and sends whatsapp notification in case of new dog'''

import datetime
import re
import os
from dotenv import load_dotenv
from connection import DB_SESSION
from models import Doggos
import smtplib, ssl

load_dotenv()

port = 465
smtp_server = os.getenv('smtp_server')
sender_email = os.getenv('sender_email')
receiver_email = os.getenv('receiver_email')
login = os.getenv('login')
password = os.getenv('password') 

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
        
        message = f"""\
        Subject: Ein neuer Hund ist im Tierheim
        
        Er heißt {dog.name} und ist ein {dog.breed}.
        Du kannst ihn dir hier anschauen {dog.link}.
        """
        
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(login, password)
            server.sendmail(sender_email, receiver_email, message)