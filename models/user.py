#!/usr/bin/python3
""" holds class User"""
# import base64
# import bcrypt
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    __tablename__ = 'users'
    if models.storage_t == 'db':
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        # if "password" in kwargs:
        #     password = kwargs["password"]
        #     salt = bcrypt.gensalt()
        #     password = bcrypt.hashpw(password.encode('utf-8'), salt)
        #     password = base64.b64encode(password).decode('utf-8')
        #     kwargs["password"] = password
        super().__init__(*args, **kwargs)
