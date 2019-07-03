'''establish database connection and create table if not existing'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

ENGINE = create_engine(r'sqlite:///doggos.db')
DB_SESSION = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=ENGINE))

Base = declarative_base()
Base.query = DB_SESSION.query_property()

def init_db():
    """ create all tables in database """
    from models import Doggos
    Base.metadata.create_all(bind=ENGINE)
