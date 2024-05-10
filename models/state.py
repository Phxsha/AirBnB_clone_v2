#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, backref

class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    
    if storage_type == 'db':
        cities = relationship("City", cascade="all, delete", backref="state")
    else:
        @property
        def cities(self):
            """Getter attribute cities that returns the list of City instances with state_id
               equals to the current State.id"""
            from models import storage
            city_list = []
            cities = storage.all(City)
            for city in cities.values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
