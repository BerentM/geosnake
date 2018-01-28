from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import Float


engine = create_engine('sqlite:///../core.db', echo=True)
metadata = MetaData()

tourDestination = Table('tourDestination', metadata,
              Column('id', Integer,primary_key=True),
              Column('name', String),
              Column('latitude', Float),
              Column('longitude', Float),
              sqlite_autoincrement=True
              )

source = Table('source', metadata,
              Column('id', Integer, primary_key=True),
              Column('post_code', String),
              Column('city', String),
              Column('street', String),
              Column('house_number', String),
              Column('latitude', Float),
              Column('longitude', Float),
              sqlite_autoincrement=True
              )

distances = Table('distances', metadata,
              Column('id', Integer, primary_key=True),
              Column('source_id', None, ForeignKey('source.id')),
              Column('destination_id', None, ForeignKey('tourDestination.id')),
              Column('distance', Float),
              sqlite_autoincrement=True
              )

metadata.create_all(engine)
