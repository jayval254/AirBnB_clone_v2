#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
import models
from state import State
import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey

class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = "cities"
    state_id = Column(String(60), nullable=False, ForeignKey(State.id))
    name = Column(String(128), nullable=False)
    places = relationship('Place', cascade='all, delete', backref='cities')
