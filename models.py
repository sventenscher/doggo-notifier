"""ORM models for dog information database table"""
from sqlalchemy import Column, String
from connection import Base


class Doggos(Base):
    """table for dog info"""
    __tablename__ = 'doggos'

    id = Column(String, primary_key=True)
    link = Column(String)
    date_added = Column(String)
    name = Column(String)
    listing_id = Column(String)
    breed = Column(String)
    in_shelter_since = Column(String)
    birthday = Column(String)
    sex = Column(String)
    size = Column(String)
    age_span = Column(String)
    last_seen_listed = Column(String)
    
    def __repr__(self):
        return f"<Doggo (name={self.name}, birthday={self.birthday})>"
    