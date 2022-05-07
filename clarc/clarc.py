from clarc import OPERATIONAL_ERROR
import sqlite3
from clarc import DB_ERROR, SUCCESS

CREATE_TABLE = '''CREATE TABLE  IF NOT EXISTS CLARC(
                           KEY CHAR(50) NOT NULL PRIMARY KEY,
                           VALUE CHAR(255) NOT NULL,
                           CREATED TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                           UPDATED TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );'''
FETCH_ALL = "SELECT * FROM CLARC LIMIT 10"
FETCH_BY_KEY = "SELECT * FROM CLARC WHERE KEY LIKE ?"
FETCH_BY_KEY_STRICT = "SELECT * FROM CLARC WHERE KEY= ?"
UPSERT_VALUE = "INSERT INTO CLARC (KEY, VALUE) VALUES(?, ?) ON CONFLICT(KEY) DO UPDATE SET VALUE= ?"
DELETE_VALUE = "DELETE FROM CLARC WHERE KEY= ?"


class DatabaseHandler:

    def __init__(self, db: sqlite3.Connection):
        self.db = db

    def is_db(self):
        try:
            self.db.cursor()
            return True
        except sqlite3.Error:
            return False

    def create_database(self) -> int:
        try:
            with self.db:
                cursor = self.db.cursor()
                cursor.execute(CREATE_TABLE)
                self.db.commit()
                return SUCCESS
        except sqlite3.Error:
            return DB_ERROR

    def init_app(self) -> int:
        database_code = self.create_database()
        if database_code != SUCCESS:
            return database_code
        return SUCCESS

    def query(self, sql: str, q=None):
        try:
            with self.db:
                cur = self.db.cursor()
                if q is None:
                    cur.execute(sql)
                else:
                    cur.execute(sql, q)
                return cur.fetchall()
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as e:
            print(e)
            return OPERATIONAL_ERROR


class Operations(DatabaseHandler):
    def __init__(self, db):
        super().__init__(db)

    def fetch_all(self):
        return super().query(FETCH_ALL)

    def fetch_key(self, key: str):
        return super().query(FETCH_BY_KEY, ('%' + key + '%',))

    def fetch_key_strict(self, key: str):
        return super().query(FETCH_BY_KEY_STRICT, (key,))

    def upsert(self, key: str, value: str):
        super().query(UPSERT_VALUE, (key, value, value))

    def delete(self, key: str):
        super().query(DELETE_VALUE, (key,))
