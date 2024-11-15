#!/usr/bin/env python3
"""
9. Expiration?
"""

import os
import datetime
from datetime import timedelta
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    will add an expiration date to a Session ID
    """
    def __init__(self):
        try:
            if not os.getenv("SESSION_DURATION"):
                self.session_duration = 0

            self.session_duration = int(os.getenv("SESSION_DURATION"))

        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Return the Session ID created
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dict = {}
        session_dict["user_id"] = self.user_id_by_session_id[session_id]
        session_dict["created_at"] = datetime.datetime.now()

        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        return user_id from the session dictionary
        """
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None

        if self.session_duration <= 0:
            return session_dict.get("user_id")

        created_at = session_dict.get("created_at")
        if created_at is None:
            return None

        session_active = created_at + timedelta(seconds=self.session_duration)

        if session_active < datetime.datetime.now():
            return None

        return session_dict.get("user_id")
