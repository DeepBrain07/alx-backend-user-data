#!/usr/bin/env python3
""" Authentication module
"""
from db import DB
from user import User
import bcrypt
import uuid


def _hash_password(password: str) -> bytes:
    """ Takes in a password string arguments and returns bytes
    """
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)
    return hashed_password


def _generate_uuid() -> str:
    """ Generates a uuid using uuid module
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Takes mandatory email and password string arguments
            and return a User object
        """
        if email and password:
            session = self._db._session
            user = session.query(User).filter_by(email=email).first()
            if user:
                raise ValueError(f'User {email} already exists')
            else:
                hashed_password = _hash_password(password)
                new_user = self._db.add_user(email, hashed_password)
                return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """ Checks for a valid login
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                hashed_password = user.hashed_password
                password = password.encode('utf-8')
                return bcrypt.checkpw(password, hashed_password)
            else:
                return False
        except Exception as e:
            return False

    def create_session(self, email: str) -> str:
        """ Returns the session id as a string
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = _generate_uuid()
                self._db.update_user(user.id, session_id=session_id)
                return session_id
            return None
        except Exception as e:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """ Returns the corresponding User
        """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            if user:
                return user
            else:
                return None
        except Exception as e:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ Destroys a session
        """
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """ Generates a UUID and update the user's
            reset_token database field
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                token = _generate_uuid()
                user.reset_token = token
                return token
            else:
                raise ValueError()
        except Exception as e:
            raise ValueError()

    def update_password(self, reset_token: str, password: str) -> None:
        """ Updates a user's password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            if user:
                hashed_password = _hash_password(password)
                user.hashed_password = hashed_password
                user.reset_token = None
                return None
            else:
                raise ValueError()
        except Exception as e:
            raise ValueError()
