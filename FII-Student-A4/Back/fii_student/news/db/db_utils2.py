from contextlib import suppress

import psycopg2
import json

from psycopg2._psycopg import IntegrityError

from news.db.populate_db import get_real_data

from configparser import ConfigParser
from news.db.anunturi_fii import get_announcements_fii
from news.db.anunturi_orar import get_announcements_orar
from news.db.anunturi_uaic import get_announcements_uaic

""" create tables in the PostgreSQL database"""


def config(filename='database.ini', section='postgresql'):
    # print(getcwd())
    # with open(filename, 'r') as fin:
    #     print(fin.read())
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def create_tables():
    commandsCreateIndex = [

        # """
        # DROP TABLE IF EXISTS news;
        # """,
        # """
        # CREATE TABLE news (
        #   news_id SERIAL PRIMARY KEY,
        #   title VARCHAR(255),
        #   body VARCHAR,
        #   author_name VARCHAR(255),
        #
        #    category VARCHAR(255),
        #    inserted_time TIMESTAMP DEFAULT now(),
        #    published_time TIMESTAMP,
        #    expire_time TIMESTAMP,
        #    source VARCHAR(255)
        #  )
        #  """
        """DROP INDEX IF EXISTS index_unique_news""" ,
        """CREATE UNIQUE INDEX index_unique_news ON news(md5(body))"""
    ]

    commands = []


    try:
        print("____________________________________________________________________")
        # get_announcements_fii()
        # get_announcements_orar()
        # get_announcements_uaic()


        for command in commandsCreateIndex:
            try:
                #print(1)
                print(command)
                params = config()
                # connect to the PostgreSQL server
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                cur.execute(command)
                cur.close()
                # commit the changes
                conn.commit()
                #conn.commit()
            except Exception as error:
                 print (error)
                # pass
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()



        commands += get_real_data()
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        print(json.dumps(commands, indent = 2))
        for command in commands:
            try:
                #print(1)

                params = config()
                # connect to the PostgreSQL server
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                cur.execute(command)
                cur.close()
                # commit the changes
                conn.commit()
                #conn.commit()
            except Exception as error:
                 print (error)
                # pass
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    # finally:
    # if conn is not None:
    #     conn.close()


if __name__ == '__main__':
    create_tables()
