#!/usr/bin/env python3
"""
20. End-to-end integration test
"""
import requests
from app import AUTH


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """
    Args:
        email: user email
        password: user password

    Tests the regestration of a user.
    """
    url = f"{BASE_URL}/users"
    data = {
            "email": email,
            "password": password
            }

    response = requests.post(url, data=data)

    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}

    response = requests.post(url, data=data)

    assert response.status_code == 400
    assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Tests Loging with wrong password
    Args:
        email: user email
        password: user password
    """
    url = f"{BASE_URL}/sessions"
    data = {
            "email": email,
            "password": password
            }
    response = requests.post(url, data=data)

    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Tests Loging with correct password
    Args:
        email: user email
        password: user password
    """
    url = f"{BASE_URL}/sessions"
    data = {
            "email": email,
            "password": password
            }
    response = requests.post(url, data=data)

    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """Test for unlogged user
    """
    url = f"{BASE_URL}/profile"
    response = requests.get(url)

    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Tests /profile end point with logged user (session_id)
    Args:
        session_id: string user session id
    """
    url = f"{BASE_URL}/profile"
    cookies = {
            "session_id": session_id
            }
    response = requests.get(url, cookies=cookies)

    assert response.status_code == 200

    user = AUTH.get_user_from_session_id(session_id)
    assert response.json() == {"email": user.email}


def log_out(session_id: str) -> None:
    """Tests the logout from logged user with seesion id
    Args:
        session_id: string user session id
    """
    url = f"{BASE_URL}/sessions"
    headers = {
        "Content-Type": "application/json"
    }
    cookies = {
            "session_id": session_id
            }
    response = requests.delete(url, headers=headers, cookies=cookies)

    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Tests /reset_password end point
    Argd:
        email: user email (string)
    Return:
        reset_token: string
    """
    url = f"{BASE_URL}/reset_password"
    data = {
            "email": email
            }

    response = requests.post(url, data=data)

    assert response.status_code == 200
    assert "email" in response.json()
    assert response.json()["email"] == email

    reset_token = response.json()["reset_token"]

    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Tests Update password endpoint
    Args:
        email: user email (string)
        reset_token: user reset token (string)
        new_password: user's new password
    """
    url = f"{BASE_URL}/reset_password"
    data = {
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password
            }

    response = requests.put(url, data=data)

    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


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
