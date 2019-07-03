"""establishes database connection, loades json data from animal shelter
 and writes data against database"""
import json
import datetime
import html

import requests
from connection import DB_SESSION, init_db
from models import Doggos
from check_dog import check_doggo

init_db()

PAYLOAD = {
    'per_page':100,
    'animal_species':'Hunde',
    'page':1,
    'animal_of_sorrow': 0
}

URL = 'https://tierschutz-berlin.de/wp-json/wp/v2/tiere'
R = requests.get(URL, params=PAYLOAD)
PAGE_COUNT = range(1, int(R.headers['X-WP-TotalPages'])+1)

for page in PAGE_COUNT:
    PAYLOAD2 = {
        'per_page':100,
        'animal_species':'Hunde',
        'page':page,
        'animal_of_sorrow': 0
    }

    R = requests.get(URL, params=PAYLOAD2)
    jdata = json.loads(R.text)

    for dog in jdata:

        record = Doggos(
            id=dog["id"],
            date_added=dog["date"],
            name=html.unescape(dog["title"]["rendered"]),
            listing_id=html.unescape(dog['acf']["single_animal_listing_ID"]),
            breed=dog['acf']["single_animal_breed"],
            in_shelter_since=dog['acf']["single_animal_shelter_entering_date"],
            birthday=html.unescape(dog['acf']["single_animal_birthday"]),
            sex=dog['acf']["single_animal_sex"],
            size=dog['acf']["single_animal_size"],
            age_span=dog['acf']["single_animal_age_span"],
            last_seen_listed=datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
            )

        DB_SESSION.add(record)
        try:
            DB_SESSION.commit()
            check_doggo(dog['id'])
        except:
            DB_SESSION.rollback()
            x = DB_SESSION.query(Doggos).get(dog['id'])
            x.last_seen_listed = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')
            DB_SESSION.commit()