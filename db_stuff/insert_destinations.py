from sqlalchemy import create_engine, MetaData
from create_db import tourDestination

engine = create_engine('sqlite:///../core.db', echo=True)
metadata = MetaData()
conn = engine.connect()

destinations =[
        {'name': 'Stare Miasto w Warszawie', \
                'latitude': 52.249107, 'longitude': 21.013725},
        {'name': 'Archikatedra gdańska', \
                'latitude': 54.41075 , 'longitude': 18.558883},
        {'name': 'Stare Miasto we Wrocławiu', \
                'latitude': 51.109367, 'longitude': 17.029709},
        {'name': 'Sukiennice w Krakowie', \
                'latitude': 50.061627, 'longitude': 19.937299},
        {'name': 'Zamek na Wawelu w Krakowie', \
                'latitude': 50.054063, 'longitude': 19.935444},
        {'name': 'Katedra Wawelska', \
                'latitude': 50.054665, 'longitude': 19.935458},
        {'name': 'Kopalnia Soli Wieliczka', \
                'latitude': 49.983504, 'longitude': 20.053818},
        {'name': 'Fabryka Oskara Schindlera', \
                'latitude': 50.047450, 'longitude': 19.961857},
        ]

for destination in destinations:
    conn.execute(tourDestination.insert(destination))

conn = engine.connect()
