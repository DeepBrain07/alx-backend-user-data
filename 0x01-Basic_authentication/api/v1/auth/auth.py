#!/usr/bin/env python3
""" This module defines the class 'Auth'
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Manages the API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Returns True if the path is not in
            the list of strings excluded_paths
        """
        if not path or not excluded_paths:
            return True
        path = path.strip('/')
        for i in range(len(excluded_paths)):
            excluded_paths[i] = excluded_paths[i].strip('/')
        if path not in excluded_paths:
            return True
        return False
    
    def authorization_header(self, request=None) -> str:
        """ Validates all requests to secure the API
        """
        if not request:
            return None
        return request.headers.get('Authorization')
    
    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns None
        """
        return None
