#!/usr/bin/env python3
""" This module inherits from the class 'Auth'
"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """ Inherits from claa Auth
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """  returns the Base64 part of the
             Authorization header for a Basic Authentication
        """
        if authorization_header is None or \
                not isinstance(authorization_header, str):
            return None
        if authorization_header[:6] != 'Basic ':
            return None
        return authorization_header[6:]
    
    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """ Returns the decoded value of a
            Base64 string base64_authorization_header
        """
        if base64_authorization_header is None or \
                not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """ Returns the user email and password from the Base64 decoded value
        """
        if decoded_base64_authorization_header is None or \
                not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        decoded_base64_authorization_header = decoded_base64_authorization_header.split(':')
        return decoded_base64_authorization_header[0], decoded_base64_authorization_header[1]
