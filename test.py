'''
Test file to run the select statements of SQL. 
'''
import configparser
import psycopg2
from select import select_queries

def check_data(cur, conn):
    '''check_data function to get samples of what's in each table'''
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