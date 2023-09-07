#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
auth = getenv("AUTH_TYPE", 'session_auth')
temp = auth
if auth == 'auth':
    auth = Auth()
elif auth == 'basic_auth':
    auth = BasicAuth()
elif auth == 'session_auth':
    auth = SessionAuth()


@app.before_request
def before_request():
    """ This code will be executed before each request
    """
    if auth:
        check = auth.require_auth(request.path,
                                    ['/api/v1/status/',
                                     '/api/v1/unauthorized/',
                                     '/api/v1/forbidden/',
                                     '/api/v1/auth_session/login/'])
        if check is True:
            if auth.authorization_header(request) is None and \
                    auth.session_cookie(request) is None:
                abort(401)
            if temp != 'session_auth':
                if auth.current_user(request) is None:
                    abort(403)

@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
