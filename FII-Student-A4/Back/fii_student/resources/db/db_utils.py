import psycopg2
# from utils.config import config
from utils.config import config
from resources.db.load_jsons import get_real_data
""" create tables in the PostgreSQL database"""


def create_tables():
    commands = [
        # """
        # BEGIN;
        #  --
        #  -- Create model Resources
        #  --
        #  DROP TABLE IF EXISTS resources;
        #  CREATE TABLE "resources" (
        #      "resources_id" serial NOT NULL PRIMARY KEY,
        #      "title" varchar(128) NOT NULL,
        #      "timestamp" timestamp with time zone NULL,
        #      "url" text,
        #      "content" text,
        #      "type" text
        #  );
        #  COMMIT;
        #  """
        # """
        # INSERT INTO resources(log_id, title, timestamp, url, content)
        #     VALUES(1, 'Ghidul Studentului UAIC', null, 'http://www.uaic.ro/studenti/ghidul-studentului-uaic/', null);
        # INSERT INTO resources(log_id, title, timestamp, url, content)
        #     VALUES(2, 'Cum iti poti verifica notele', null, 'http://www.uaic.ro/studenti/cum-iti-poti-verifica-notele/', null);
        # INSERT INTO resources(log_id, title, timestamp, url, content)
        #     VALUES(3, 'Reprezentarea studentilor in structurile de conducere', null, 'http://www.uaic.ro/studenti/reprezentarea-studentilor-structurile-de-conducere-2/', null);
        # INSERT INTO resources(log_id, title, timestamp, url, content)
        #     VALUES(4, 'Orientare in Cariera, Insertie Profesionala si Alumni', null, 'http://www.uaic.ro/studenti/cariera/', null);
        # INSERT INTO resources(log_id, title, timestamp, url, content)
        #     VALUES(5, 'Burse', null, 'http://www.uaic.ro/studenti/burse/', null);
        # INSERT INTO resources(log_id, title, timestamp, url, content)
        #     VALUES(6, 'Cazare', null, 'http://www.uaic.ro/studenti/cazare/', null);
        # INSERT INTO resources(log_id, title, timestamp, url, content)
        #     VALUES(7, 'Mobilitati academice pentru studenti', null, 'http://www.uaic.ro/studenti/mobilitati-academice-pentru-studenti/', null);
        # INSERT INTO resources(log_id, title, timestamp, url, content)
        #     VALUES(8, 'Cantinele Universitatii', null, 'http://www.uaic.ro/studenti/cantinele-universitatii-alexandru-ioan-cuza/', null);
        # INSERT INTO resources(log_id, title, timestamp, url, content)
        #     VALUES(9, 'Servicii Medicale', null, 'http://www.uaic.ro/studenti/servicii-medicale/', null);
        # INSERT INTO resources(log_id, title, timestamp, url, content)
        #     VALUES(10, 'Biblioteci', null, 'http://www.uaic.ro/studenti/biblioteci/', null);
        # """
        """DROP INDEX IF EXISTS index_unique_resources_url""",
        """DROP INDEX IF EXISTS index_unique_resources_content""",
        """CREATE UNIQUE INDEX index_unique_resources_url ON resources(md5(url))""",
        """CREATE UNIQUE INDEX index_unique_resources_content ON resources(md5(content))"""
    ]
    try:
        # read the connection parameters

        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        commands += get_real_data()
        # create table one by one
        for command in commands:

            try:
                params=config()
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                #print(command)
                cur.execute(command)
                cur.close()
                conn.commit()


            except Exception as error:
                 print (error)
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