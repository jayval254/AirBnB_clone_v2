#!/usr/bin/python3
"""Defines ``DBStorage`` class """

from models.base_model import Basemodel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import os
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import scoped_session
from os import getenv

all_classes = {'State': State, 'City': City,
               'User': User, 'Place': Place,
               'Review': Review, 'Amenity': Amenity}


class DBStorage:
    """Storage class that connects the application to a database """
    __engine = None
    __session = None

    def __init__(self):
        """Constructor method """
         # create engine
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'.
                                      format(getenv('HBNB_MYSQL_USER'),
                                             getenv('HBNB_MYSQL_PWD'),
                                             getenv('HBNB_MYSQL_HOST'),
                                             getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)

        # drop tables if test environment
        if getenv('HBNB_ENV') == 'test':
                Base.metadata.drop_all(self.__engine)
            

    def all(self, cls=None):
        """Query objects on the current database session """
         obj_dict = {}

        if cls:
            for row in self.__session.query(cls).all():
                # populate dict with objects from storage
                obj_dict.update({'{}.{}'.
                                format(type(cls).__name__, row.id,): row})
        else:
            for key, val in all_classes.items():
                for row in self.__session.query(val):
                    obj_dict.update({'{}.{}'.
                                    format(type(row).__name__, row.id,): row})
        return obj_dict

    def new(self, obj):
        """Add object to current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from database session
        """
        if obj:
            # determine class from obj
            cls_name = all_classes[type(obj).__name__]

            # query class table and delete
            self.__session.query(cls_name).\
                filter(cls_name.id == obj.id).delete()

    def reload(self):
        """Create database session"""
        # create session from current engine
        Base.metadata.create_all(self.__engine)
        # create db tables
        session = sessionmaker(bind=self.__engine,
                               expire_on_commit=False)
        # previousy:
        # Session = scoped_session(session)
        self.__session = scoped_session(session)

    def close(self):
        """Close scoped session
        """
        self.__session.remove()
