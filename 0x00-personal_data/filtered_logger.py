#!/usr/bin/env python3
"""
0. Regex-ing
"""


import re
from typing import List
import logging
import os
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
         Method to filter values in incoming log records
         using filter_datum.
        """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str,
                 message: str,
                 separator: str) -> str:
    """
     returns the log message obfuscated
    """
    for field in fields:
        message = re.sub(f'{field}=(.*?){separator}',
                         f'{field}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """
    returns a logging.Logger object.
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)

    formatter = RedactingFormatter(list(PII_FIELDS))
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    returns a connector to the database
    """
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db = os.getenv('PERSONAL_DATA_DB_NAME')

    connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=db
            )

    return connection


def main() -> None:
    """
    Obtain a database connection using get_db and retrieve
    all rows in the users table and display each row under
    a filtered format.
    """
    db_connection = get_db()

    cursor = db_connection.curtor()
    cursor.execute('SELECT * FROM users;')

    rows = cursor.fetchall()

    logger = get_logger()

    for row in rows:
        message = "; ".join([f"{field}={row[field]}" for field in row.keys()])

        formated_msg = filter_datum(PII_FIELDS,
                                    RedactingFormatter.REDACTION,
                                    message,
                                    RedactingFormatter.SEPARATOR)
        logger.info(formated_msg)

    cursor.close()
    db_connection.close()


if __name__ == "__main__":
    main()
