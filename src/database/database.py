import psycopg2
from psycopg2 import DatabaseError
from decouple import config


# funcion para conexion a BD
def get_connection():
    try:
        return psycopg2.connect(
            host=config("SQL_HOS"),
            user=config("SQL_USER"),
            password=config("SQL_PASSWORD"),
            database=config("SQL_DATABASE"),
        )
    except DatabaseError as ex:
        raise ex
