import configparser
import psycopg2
from select import select_queries

def check_data(cur, conn):
    for query in select_queries:
        cur.execute(query)
        records = cur.fetchall()
        for row in records:
            print(row)
        print()
        conn.commit()

def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    check_data(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()