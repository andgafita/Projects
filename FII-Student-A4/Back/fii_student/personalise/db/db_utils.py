import psycopg2
from utils.config import config

""" create tables in the PostgreSQL database"""


def create_tables():
    commands = (
       """
       DROP TABLE IF EXISTS personalise_app;
       """,
       """
       CREATE TABLE news (
         -- model fields here
        )
        """, """
        # insert values here
        """
        )
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()
