#!/usr/bin/env python3
"""
API authentication
"""


from flask import request
from typing import List, TypeVar
import os


class Auth:
    """
    Manages the API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        returns True if the path is not in the list of
        strings excluded_paths.
        """
        if path is None or excluded_paths is None:
            return True
        if path[-1] != '/':
            path += '/'
        for ex_path in excluded_paths:
            if ex_path[-1] == "*" and ex_path[: -1] in path:
                return False
            if path == ex_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Validates all requests to secure the API
        """
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Checks for the current user
        """
        return None

    def session_cookie(self, request=None) -> str:
        """
        returns a cookie value from a request
        """
        if request is None:
            return None
        session = os.getenv("SESSION_NAME")
        return request.cookies.get(session)
