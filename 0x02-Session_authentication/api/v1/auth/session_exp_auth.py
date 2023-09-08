#!/usr/bin/env python3
""" This module inherits from the class 'SessionnAuth'
"""
from os import getenv
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ Inherits from SessionAuth
    """
    session_dictionary = {}

    def __init__(self):
        """ Overloads __init__
        """
        try:
            SESSION_DURATION = int(getenv('SESSION_DURATION', 60))
        except Exception as e:
            SESSION_DURATION = 0
        if not SESSION_DURATION:
            SESSION_DURATION = 0
        self.session_duration = SESSION_DURATION

    def create_session(self, user_id=None):
        """ Overloads create_session
        """
        try:
            session_id = super().create_session(user_id)
        except Exception as e:
            return None
        self.session_dictionary['user_id'] = user_id
        self.session_dictionary['created_at'] = datetime.now()
        self.user_id_by_session_id[session_id] = self.session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Overloads user_id_for_session_id
        """
        if not session_id:
            return None
        if not self.user_id_by_session_id.get(session_id):
            return None
        if self.session_duration <= 0 :
            return self.session_dictionary.get('user_id')
        if self.session_dictionary.get('created_at') is None:
            return None
        time_used = timedelta(self.session_duration) + self.session_dictionary.get('created_at')
        if time_used < datetime.now():
            return None
        return self.session_dictionary.get('user_id')
