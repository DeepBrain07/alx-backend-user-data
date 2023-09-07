#!/usr/bin/env python3
""" This module inherits from the class 'Auth'
"""
from os import getenv
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """ Inherits from class Auth
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a Session ID for a user_id
        """
        if not user_id:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User ID based on a Session ID
        """
        if not session_id or not isinstance(session_id, str):
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None):
        """ Returns a User instance based on a cookie value
        """
        if request is None:
            return None
        cookie_value = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie_value)
        return User.get(user_id)
    
    def destroy_session(self, request=None):
        """ Deletes the user session / logout
        """
        if not request:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user = self.user_id_for_session_id(session_id)
        if not user:
            return False
        self.user_id_by_session_id.pop(session_id)
