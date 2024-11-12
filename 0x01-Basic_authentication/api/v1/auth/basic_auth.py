#!/usr/bin/env python3
"""
6. Basic auth
"""

from api.v1.auth.auth import Auth
import base64
from models.user import User
from models.base import Base
from typing import TypeVar


class BasicAuth(Auth):
    """
    Basic Authentication
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Returns the Base64 part of the Authorization
        header for a Basic Authentication.
        """
        if authorization_header is None or not isinstance(
                authorization_header, str):
            return None
        if (not authorization_header.startswith("Basic ")):
            return None
        """ Return the value after Basic (after the space) """
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes base64_authorization_header using Base64
        """
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None
        try:
            byte_str = base64.b64decode(base64_authorization_header)
            return byte_str.decode('utf-8')

        except (UnicodeDecodeError, base64.binascii.Error):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Returns the user email and password from the
        Base64 decoded value.
        """
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        user_info = decoded_base64_authorization_header.split(":")
        return (user_info[0], user_info[1])

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on his email and
        password.
        """
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
        except Exception:
            return None

        if not users or len(users) == 0:
            return None

        user = users[0]

        if user.is_valid_password(user_pwd):
            return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Overloads Auth and retrieves the User
        instance for a reques.
        """
        auth_haeder = self.authorization_header(request)
        b64_header = self.extract_base64_authorization_header(auth_haeder)
        decoded_b64 = self.decode_base64_authorization_header(b64_header)
        user_credentials = self.extract_user_credentials(decoded_b64)
        user = self.user_object_from_credentials(
                user_credentials[0], user_credentials[1])
        return user
