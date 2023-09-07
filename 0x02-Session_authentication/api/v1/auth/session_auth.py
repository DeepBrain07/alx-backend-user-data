#!/usr/bin/env python3
""" This module inherits from the class 'Auth'
"""
from os import getenv
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User
from api.v1.views import app_views
from flask import request, jsonify


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
        print(user_id)
        return User.get(user_id)

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """ login
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({ "error": "email missing" }), 400
    if not password:
        return jsonify({ "error": "password missing" }), 400
    users = User.search({'email': email})
    if not users or users == []:
        return jsonify({ "error": "no user found for this email" }), 400
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth

            session_id = auth.create_session(user.to_json().get('id'))
            SESSION_NAME = getenv("SESSION_NAME")
            response = jsonify(user.to_json())
            response.set_cookie(SESSION_NAME, session_id)
            return response

    return jsonify({ "error": "wrong password" }), 401
