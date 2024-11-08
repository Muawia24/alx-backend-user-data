#!/usr/bin/env python3
"""
5. Encrypting passwords
"""


import bcrypt


def hash_password(password: str) -> bytes:
    """
    returns a salted, hashed password, which is a byte string.
    """
    salt = bcrypt.gensalt()
    bytes = password.encode('utf-8')

    return bcrypt.hashpw(bytes, salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    b_pass = password.encode('utf-8')
    return bcrypt.checkpw(
            b_pass,
            hashed_password
            )
