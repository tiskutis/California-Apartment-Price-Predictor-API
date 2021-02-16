import os
import psycopg2
from psycopg2 import OperationalError, DatabaseError
import sys


def print_psycopg2_exception(err):
    """
    This method provides additional information about the passed error:
        - details about the exception
        - line number where exception occurred
        - diagnostics
        - pgcode
        - pgerror
    :param err: error from PostgreSQL database
    :return: None
    """
    err_type, err_obj, traceback = sys.exc_info()
    line_num = traceback.tb_lineno

    print("\npsycopg2 ERROR:", err, "on line number:", line_num)
    print("psycopg2 traceback:", traceback, "-- type:", err_type)
    print("\nextensions.Diagnostics:", err.diag)
    print("pgerror:", err.pgerror)
    print("pgcode:", err.pgcode, "\n")


def get_connection():
    """
    Connects to PostgreSQL database and returns connection object
    :return: connection object or None
    """
    try:
        conn = psycopg2.connect(os.environ['DATABASE_URL'])

    except OperationalError as err:
        print_psycopg2_exception(err)
        conn = None

    return conn


def create_table() -> None:
    """
    Creates table in the database with requests and responses columns
    :return: None
    """
    try:
        conn = get_connection()

        if conn is not None:
            cursor = conn.cursor()
            statement = "CREATE TABLE IF NOT EXISTS lr (id bigserial PRIMARY KEY, " \
                        "requests VARCHAR(8000), responses VARCHAR(8000))"
            cursor.execute(statement)
            conn.commit()

    except DatabaseError as err:
        print_psycopg2_exception(err)


def drop_tables() -> None:
    """
    Used for dropping tables from the database
    :return: None
    """
    try:
        conn = get_connection()

        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS lr")

    except DatabaseError as err:
        print_psycopg2_exception(err)


def insert_in_table(input_request: str, output_response: str) -> None:
    """
    Inserts request and response into the database
    :param input_request: request sent by the client (inputs)
    :param output_response: response given by the server (predictions)
    :return: None
    """
    try:
        conn = get_connection()

        if conn is not None:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO lr (requests, responses) values ('{input_request}', '{output_response}')")
            conn.commit()

    except DatabaseError as err:
        print_psycopg2_exception(err)


def select_from_table() -> list:
    """
    Selects 10 most recent requests and responses from the database
    :return: list of 10 most recent requests and responses from the database
    """
    try:
        conn = get_connection()

        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM lr ORDER BY id DESC LIMIT 10")
            return cursor.fetchall()

    except DatabaseError as err:
        print_psycopg2_exception(err)
