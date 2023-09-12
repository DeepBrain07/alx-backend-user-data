#!/usr/bin/env python3
""" This module defines the user database
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *


Base = declarative_base()


class User(Base):
    """ The user model
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
