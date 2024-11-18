#!/usr/bin/env python3
"""
4. Hash password
"""


import bcrypt
from db import DB
from user import User
from typing import TypeVar
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Args:
        password string arguments
    Returns:
         bytes.
    """
    encoded_pwd = password.encode("utf-8")
    hash_pwd = bcrypt.hashpw(encoded_pwd, bcrypt.gensalt())

    return hash_pwd


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar('User'):
        """
        Args:
            email and password string arguments
        Returns:
            User object.
        """
        try:
            user = self._db.find_by(email=email)
        except NoResultFound:
            user = self._db.add_user(email, _hash_password(password))
        else:
            raise ValueError('User <user\'s email> already exists')
