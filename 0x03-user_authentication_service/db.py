#!/usr/bin/env python3
"""DB module
"""


import logging
from typing import Dict

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User

logging.disable(logging.WARNING)


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
         two required string arguments: email and
         hashed_password, and returns a User object
        """
        user = User(email=email, hashed_password=hashed_password)
        try:
            self._session.add(user)
            self._session.commit()

        except Exception as e:
            print(f"Error adding user to database: {e}")
            self._session.rollback()
            raise

        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Args:
            arbitrary keyword arguments
        Returns:
            returns the first row found in the users table
            as filtered by the method's input arguments.
        """
        if not kwargs:
            raise InvalidRequestError("No filter provided for the query")
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound("No Result Found")
        except InvalidRequestError:
            raise InvalidRequestError("Wrong query arguments are passed")

    def update_user(self, user_id, **kwargs) -> None:
        """
        Args:
            user_id integer and arbitrary keyword arguments
        Returns:
            None
        """
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError(f"User with id {user.id} not found")

        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"Invalid attribute: {key}")
            setattr(user, key, value)

        self._session.commit()
