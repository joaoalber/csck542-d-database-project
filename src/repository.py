import pymysql

class MySQLRepository:
    def __init__(self):
        self.conn = pymysql.connect(
            host="127.0.0.1",
            user="dev_user",
            password="123456",
            database="university",
            cursorclass=pymysql.cursors.DictCursor  # optional but useful
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