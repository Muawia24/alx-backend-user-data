#!/usr/bin/env python3
"""
6. Basic Flask app
"""


from flask import Flask, jsonify, request, abort, redirect, url_for

from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def home():
    """
    Returns:
        {"message": "Bienvenue"}
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """
    POST /users
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})

    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """
    POST /sessions
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        return abort(401)

    return jsonify({"email": "<user email>", "message": "logged in"})


@app.route('/sessions', methods=['DELETE'])
def logout():
    """
    DELETE /sessions
    """
    session_id = request.cookies.get('session_id')

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    AUTH.destroy_session(user.id)

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
