#!/usr/bin/env python3
""" Module of Session Authentication views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    POST /auth_session/login
    Return:
        dictionary representation of user if found else
        error message
    """
    email = request.form.get('email')
    if email is None:
        return jsonify({"error": "email missing"}), 400

    pwd = request.form.get('password')
    if pwd is None:
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({"email": email})
    except Exception:
        return None
    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]

    if not user.is_valid_password(pwd):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    session_id = auth.create_session(user.id)

    session_name = os.getenv("SESSION_NAME")
    response = jsonify(user.to_json())
    response.set_cookie(session_name, session_id)

    return response


@app_views.route(
        '/auth_session/logout',
        methods=['DELETE'], strict_slashes=False)
def logout():
    """
    DELETE /api/v1/auth_session/logout
    Return:
        Empty json dictionary in success or error
    """
    from api.v1.app import auth

    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200
