#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User
from typing import TypeVar


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

    def add_user(self, email: str, hashed_password: str) -> TypeVar('User'):
        """
         two required string arguments: email and
         hashed_password, and returns a User object
        """
        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()

            return user

        except Exception:
            self._session.rollback()
            user = None

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
        user = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"Invalid attribute: {key}")
            setattr(user, key, value)

        self._session.commit()