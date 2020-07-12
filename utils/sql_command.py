import mysql.connector

from mysql.connector.connection import MySQLConnection
from mysql.connector import pooling

from eigenfactor_crawler.config import project_config

import os, sys

pool = None

def init_pool():
    global pool
    name = 'JOURNAL'

    database_config = project_config.CONFIG['DATABASE'][name]
    print("PID %d: initializing pool..." % os.getpid())
    pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="test",
                                    pool_size=4,
                                    pool_reset_session=True,
                                    host=database_config['HOST'],
                                    database=database_config['NAME'],
                                    user=database_config['USER'],
                                    password=database_config['PASSWORD'],
                                    port=database_config['PORT'],
                                    use_unicode=True,
                                    charset='utf8',
                                    connect_timeout=60 * 30
                                )



def updatedb(config, name):
    conn = conn2db(config, name)
    curr = conn.cursor()

    try:
        sql = ('Alter TABLE Eigenfactor RENAME TO Eigenfactor_bkp')
        curr.execute(sql)
    except:
        print('Table Eigenfactor not Exists or Eigenfactor_bkp already exists')
        sys.exit(1)

    sql = project_config.TABLE_COLUMNS
    curr.execute(sql)

    curr.close()
    conn.close()


def conn2db(config, name):
    database_config = config['DATABASE'][name]
    connect = mysql.connector.connect(
        user=database_config['USER'],
        password=database_config['PASSWORD'],
        host=database_config['HOST'],
        database=database_config['NAME'],
        port=database_config['PORT'],
        use_pure=False,
        use_unicode=True,
        charset='utf8',
        connect_timeout=60 * 30
    )
    return connect


def select_query(connect, sql, parameter, multi=False):
    cursor = connect.cursor()
    try:
        if parameter:
            cursor.execute(sql % parameter)
        else:
            cursor.execute(sql)
        result = cursor.fetchall() if multi else cursor.fetchone()
        connect.commit()
    except mysql.connector.Error:
        raise
    else:
        if result:
            return result
        else:
            return None
    finally:
        cursor.close()


def execute_query(connect, sql, parameter, many=False):
    cursor = connect.cursor()
    try:
        if many:
            cursor.executemany(sql, parameter)
        else:
            cursor.execute(sql, parameter)
        connect.commit()
    except mysql.connector.Error:
        raise
    finally:
        cursor.close()
