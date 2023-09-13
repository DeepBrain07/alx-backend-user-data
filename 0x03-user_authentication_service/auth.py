#!/usr/bin/env python3
""" Authentication module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """ Takes in a password string arguments and returns bytes
    """
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)
    return hashed_password
