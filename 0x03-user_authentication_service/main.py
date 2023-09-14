#!/usr/bin/env python3
""" Main module
"""
import requests


def register_user(email: str, password: str) -> None:
    """ Tests register user endpoint
    """
    data = {'email': email, 'password': password}
    response = requests.post('localhost:5000/users', data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """ Tests login endpoint
    """
    data = {'email': email, 'password': password}
    response = requests.post('localhost:5000/sessions', data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """ Tests login endpoint
    """
    data = {'email': email, 'password': password}
    response = requests.post('localhost:5000/sessions', data=data)
    assert response.json() == {"email": email, "message": "logged in"}


def profile_unlogged() -> None:
    """ Tests profile endpoint
    """
    response = requests.get('localhost:5000/profile')
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """ Tests profile endpoint
    """
    cookies = {'session_id': session_id}
    response = requests.get('localhost:5000/profile', cookies=cookies)
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """ Tests logout endpoint
    """
    cookies = {'session_id': session_id}
    response = requests.delete('localhost:5000/sessions', cookies=cookies)
    assert response.url == 'localhost:5000/'


def reset_password_token(email: str) -> str:
    """ Tests reset_password_token endpoint
    """
    data = {'email': email}
    response = requests.post('localhost:5000/reset_password', data=data)
    assert response.status_code == 200
    assert response.json().get('email') == email


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Tests update_password endpoint
    """
    data = {'email': email, 'reset_token': reset_token,
            'new_password': new_password}
    response = requests.put('localhost:5000/reset_password', data=data)
    assert response.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
