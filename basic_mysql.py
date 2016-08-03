

import MySQLdb
from DBUtils.PooledDB import PooledDB


class mysqlConf:

    user = ""
    password = ""
    host = ""
    db = ""
    pass

class Mysql(object):

    def __init__(self, *args, **kwargs):
        pass

    def fetchall(self, query, params=None, commit=True):
        count = self._cursor.execute(query, params)
        records = self._cursor.fetchall()
        if commit:
            self._connect.commit()
        return list(records)

    def fetchone(self, query, params=None, commit=True):
        count = self._cursor.execute(query, params)
        record = self._cursor.fetchone()
        if commit:
            self._connect.commit()
        return record

    def execute(self, query, params=None):
        count = self._cursor.execute(query, params)
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self._conn.commit()
        else:
            #记录下错误信息
            logging.info("")
            self._conn.rollback()


def fetchall():
    pass

def fetchone():
    pass