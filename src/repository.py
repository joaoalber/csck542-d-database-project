import pymysql

class MySQLRepository:
    def __init__(self):
        self.conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,                 # XAMPP default port
            user="root",               # root user for local setup
            password="",               # empty password (default in XAMPP)
            database="University",     # must match your phpMyAdmin DB name
            cursorclass=pymysql.cursors.DictCursor
        )

    def execute(self, query, params=None):
        cursor = self.conn.cursor()
        cursor.execute(query, params or ())
        self.conn.commit()
        cursor.close()

    def select(self, query, params=None):
        cursor = self.conn.cursor()
        cursor.execute(query, params or ())
        results = cursor.fetchall()
        cursor.close()
        return results

    def close(self):
        if self.conn and self.conn.open:
            self.conn.close()
