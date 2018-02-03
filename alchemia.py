from sqlalchemy import create_engine, MetaData, func, desc, Table, func
from sqlalchemy.sql import select, and_, or_, not_
import response  
import distance


class DBHelper():
    def __init__(self):
        engine = create_engine('sqlite:///core.db',
                connect_args={'check_same_thread': False}, echo=False)
        metadata = MetaData()
        self.tourDestination = Table('tourDestination', metadata, autoload=True, autoload_with=engine)
        self.source = Table('source', metadata, autoload=True, autoload_with=engine)
        self.distances = Table('distances', metadata, autoload=True, autoload_with=engine)
        self.conn = engine.connect()
    
    def checkSource(self,post_code,city,street,house_number):
        """Sprawdzenie czy punkt poczatkowy jest już w bazie"""
        output = []
        s = select([self.source.c.id]).where(
                    and_(
                        self.source.c.post_code==post_code,
                        self.source.c.city==city,
                        self.source.c.street==street,
                        self.source.c.house_number==house_number
                        ))
        r = self.conn.execute(s)
        for row in r:
            output.append(row)
        try:
            return max(output)
        except Exception:
            return False

    def insertSource(self, post_code='', city='', street='', house_number=''):
        """Dodawanie nowego punktu początkowego do bazy danych
        i uzupełnianie danych o dł i szer geograficzną"""
        resp = response.lat_lon(post_code, city, street, house_number)
        ins = self.source.insert().values( \
                post_code=post_code, city=city, street=street, \
                house_number=house_number, \
                latitude=resp['lat'], longitude=resp['lon'] \
                )
        self.conn.execute(ins)

    def insertDestination(self, name='', latitude=None, longitude=None):
        """Dodaj nowy punkt docelowy"""
        ins = self.tourDestination.insert().values(\
                name=name, latitude=latitude, longitude=longitude\
                )
        self.conn.execute(ins)

    def getDestinations(self, source_id=None):
        """Lista wszycstkich punktów docelowych"""
        output = []
        if source_id:
            lastId = source_id
        else:
            lastId = select([func.max(self.source.c.id)])
        s = select([self.tourDestination.c.name,
            self.tourDestination.c.latitude, self.tourDestination.c.longitude,
            self.distances.c.distance]).where(
                    and_(
                        self.distances.c.source_id==lastId,
                        self.tourDestination.c.id==self.distances.c.destination_id
                        )).distinct()
        r = self.conn.execute(s)
        for row in r:
            output.append(row)
        return output 

    def getLastSource(self, source_id=None):
        """Ostatnio wprowadzony punkt poczatkowy"""
        output = []
        if source_id:
            lastId = source_id
        else:
            lastId = select([func.max(self.source.c.id)])
        s = select([self.source]).where(self.source.c.id
            == lastId)
        r = self.conn.execute(s)
        for row in r:
            output.append(row)
        return output

    def calculateDistance(self, source_id=None):
        """Insert do tabeli distances, obliczenie odległości"""
        #TODO: uproscic lub podzielic ta funkcje
        if source_id:
            lastId = source_id
        else:
            lastId = select([func.max(self.source.c.id)])
        s = select([self.source.c.latitude,
            self.source.c.longitude, self.source.c.id]).where(
                        self.source.c.id==lastId
                        )
        r = self.conn.execute(s)
        for row in r:
            lat1 = row[0]
            lon1 = row[1]
            source_id = row[2]

        s2 = select([self.tourDestination.c.latitude,
            self.tourDestination.c.longitude,
            self.tourDestination.c.id]).distinct()
        r2 = self.conn.execute(s2)
        s3 = select([self.distances.c.source_id,
            self.distances.c.destination_id]).where(self.distances.c.source_id==lastId)
        r3 = self.conn.execute(s3)
        distancesList = []
        for row3 in r3: 
            distancesList.append(row3)
        print(distancesList)
        ins = []
        for row2 in r2:
            lat2 = row2[0]
            lon2 = row2[1]
            destination_id = row2[2]
            if (source_id, destination_id) not in distancesList:
                """Sprawdzenie czy para id znajduje sie juz w bazie"""
                dist = distance.distance(lat1, lon1, lat2, lon2)
                ins.append({'source_id': source_id, \
                    'destination_id': destination_id, \
                    'distance': dist})
                print(ins)
        self.conn.execute(self.distances.insert(), ins)
