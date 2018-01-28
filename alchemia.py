from sqlalchemy import create_engine, MetaData, func, desc, Table
from sqlalchemy.sql import select, and_, or_, not_
import response  
import distance


class Database():
    def __init__(self):

        engine = create_engine('sqlite:///core.db', echo=False)
        metadata = MetaData()
        self.tourDestination = Table('tourDestination', metadata, autoload=True, autoload_with=engine)
        self.source = Table('source', metadata, autoload=True, autoload_with=engine)
        self.distances = Table('distances', metadata, autoload=True, autoload_with=engine)
        self.conn = engine.connect()
    
    def insertSource(self, post_code='', city='', street='', house_number=''):
        """Dodawanie nowej lokalizacji poczatkowej do bazy danych
        i uzupełnianie danych o dł i szer geograficzną"""
        resp = response.lat_lon(post_code, city, street, house_number)
        ins = self.source.insert().values( \
                post_code=post_code, city=city, street=street, \
                house_number=house_number, \
                latitude=resp['lat'], longitude=resp['lon'] \
                )
        self.conn.execute(ins)

    def calculateDistance(self, post_code, city, street, house_number,
            destination_name):
        """Insert do tabeli distances, obliczenie odległości"""

        # TODO: rozbić funkcję na mniejsze, połączyć ją z funcją insertSource
        s = select([self.source.c.latitude,
            self.source.c.longitude, self.source.c.id]).where(
                    and_(
                        self.source.c.post_code==post_code,
                        self.source.c.city==city,
                        self.source.c.street==street,
                        self.source.c.house_number==house_number
                        ))
        r = self.conn.execute(s)

        for row in r:
            lat1 = row[0]
            lon1 = row[1]
            source_id = row[2]

        s2 = select([self.tourDestination.c.latitude,
            self.tourDestination.c.longitude, self.tourDestination.c.id]).where(self.tourDestination.c.name==destination_name)

        r2 = self.conn.execute(s2)
        for row2 in r2:
            lat2 = row2[0]
            lon2 = row2[1]
            destination_id = row2[2]
       
        dist = distance.distance(lat1, lon1, lat2, lon2)
        ins = self.distances.insert().values( \
                source_id=source_id, \
                destination_id=destination_id, \
                distance=dist
                )
        self.conn.execute(ins)
        print(dist)
        
