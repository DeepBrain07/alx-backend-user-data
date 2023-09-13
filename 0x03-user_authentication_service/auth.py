#!/usr/bin/env python3
""" Authentication module
"""
from db import DB
from user import User
import bcrypt


def _hash_password(password: str) -> bytes:
    """ Takes in a password string arguments and returns bytes
    """
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Takes mandatory email and password string arguments
            and return a User object
        """
        session = self._db._session
        user = session.query(User).filter_by(email=email).first()
        if user:
            raise ValueError(f'User {email} already exists')
        else:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user
