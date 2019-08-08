'''establish database connection'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
#from sqlalchemy.ext.declarative import declarative_base

ENGINE = create_engine(r'sqlite:///doggos.db')
DB_SESSION = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=ENGINE))
