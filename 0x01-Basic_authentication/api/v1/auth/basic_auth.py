#!/usr/bin/env python3
"""
6. Basic auth
"""

from api.v1.auth.auth import Auth


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
