#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Adds a user to the database
        """
        if email and hashed_password:
            session = self._session
            new_user = User(email=email, hashed_password=hashed_password)
            session.add(new_user)
            session.commit()
            return new_user

    def find_user_by(self, **kwargs) -> User:
        """ Find a user by the input argument
        """
        session = self._session
        for key, val in kwargs.items():
            filter_condition = {key: val}
            user = session.query(User).filter_by(**filter_condition).first()
            if not user:
                raise NoResultFound()
            return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Updates a user's data
        """
        session = self._session
        user = self.find_user_by(id=user_id)
        for key, val in kwargs.items():
            if key not in dir(user):
                raise ValueError()
            setattr(user, key, val)
        session.commit()
