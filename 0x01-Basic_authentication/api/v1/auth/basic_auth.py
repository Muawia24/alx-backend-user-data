#!/usr/bin/env python3
"""
6. Basic auth
"""

from api.v1.auth.auth import Auth
import base64


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

        except base64.binascii.Error:
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
