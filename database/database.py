import sqlite3
from setting import DATABASE_NAME
from .exeptiondb import StudentDbException
from typing import Protocol

class Database(Protocol):
    def __init__(self):
        pass
    
    def execute(self, sql: str, params: tuple = None) -> sqlite3.Cursor:
        pass

    def commit(self):
        pass

    @property
    def cursor(self):
        pass

    @cursor.setter
    def cursor(self, cursor):
        pass

    @property
    def conn(self):
        pass

    @conn.setter
    def conn(self, conn):
        pass
    
    


class StudentDb(Database):
    def __init__(self):
        try:
            self.conn = sqlite3.connect(DATABASE_NAME)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            raise StudentDbException(e)
    
    @property
    def cursor(self):
        return self.__cursor
    
    @cursor.setter
    def cursor(self, value):
        self.__cursor = value

    @property
    def conn(self):
        return self.__conn
    
    @conn.setter
    def conn(self, value):
        self.__conn = value
        

    def __del__(self):
        self.conn.close()
    


def get_db():
    return StudentDb()