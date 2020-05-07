'''
File to call queries to get staging data and then insert it into the songplays, users, 
songs, artists, & time tables. It relies on dwh.cfg which is to be provided by user see
README.md for more details.
'''
import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    '''load_staging_tables copies raw data to the staging table so that it can go through etl process'''
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    '''insert_tables runs the etl queries that will see data transformed into a star schema'''
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()