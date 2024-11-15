#!/usr/bin/env python3
"""
10. Sessions in database
"""

from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    Sessions in database
    """
    def create_session(self, user_id=None):
        """
        creates and stores new instance of UserSession and returns the
        Session ID
        """
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        kwargs = {"user_id": user_id, "session_id": session_id}
        user_session = UserSession(**kwargs)
        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
         returns the User ID by requesting UserSession in
         the database based on session_id
        """
        try:
            user = UserSession.search({"session_id": session_id})
        except Exception:
            return None

        if len(user) <= 0:
            return None

        time_span = timedelta(seconds=self.session_duration)
        exp_time = user[0].created_at + time_span

        if exp_time < datetime.now():
            return None

        return user[0].user_id

    def destroy_session(self, request=None):
        """
        destroys the UserSession based on the Session ID
        from the request cookie
        """
        session_id = self.session_cookie(request)

        if not session_id:
            return False

        user_session = UserSession.search({"session_id": session_id})
        if user_session:
            user_session[0].remove()
            return True
        return False
