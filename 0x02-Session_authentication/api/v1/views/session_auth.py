#!/usr/bin/env python3
""" Module of session_auth views
"""
from os import getenv
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User


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
            SESSION_NAME = getenv("SESSION_NAME", '_my_session_id')
            response = jsonify(user.to_json())
            response.set_cookie(SESSION_NAME, session_id)
            return response

    return jsonify({ "error": "wrong password" }), 401

@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def session_logout():
    """ logout
    """
    from api.v1.app import auth
    destroy_session = auth.destroy_session(request)
    if destroy_session is False:
        abort(404)
    return jsonify({}), 200
