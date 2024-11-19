#!/usr/bin/env python3
"""
4. Hash password
"""


import bcrypt
import uuid
from db import DB
from user import User
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


def _generate_uuid() -> str:
    """
    Returns a string representation of a new UUID.
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Args:
            email and password string arguments
        Returns:
            User object.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = self._db.add_user(email, _hash_password(password))
            return user
        else:
            raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """
        Args:
            email and password required arguments
        Returns:
             check the password with bcrypt.checkpw. If it
             matches return True. In any other case,
             return False.
        """
        try:
            user = self._db.find_user_by(email=email)
            bytes_pwd = password.encode('utf-8')
            if bcrypt.checkpw(bytes_pwd, user.hashed_password):
                return True
            else:
                return False

        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Args:
            email: string argument
        Returns:
            session ID as a string.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)

        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Args:
            session_id: string
        Returns:
            returns the corresponding User or None.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """
        Args:
            user_id: integer
        Return:
            None, updates the corresponding user's session
            ID to None
        """
        if user_id is None:
            return None

        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        Args:
            email: string
        Returns:
            string token
        Finds the user corresponding to the email. If the
        user does not exist, raise a ValueError exception.
        If it exists, generate a UUID and update the user's
        reset_token database field. Return the token.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError("User corresponding to this email is not found")

        reset_token = _generate_uuid()
        self._db.update(user.id, reset_token=reset_token)

        return reset_token
