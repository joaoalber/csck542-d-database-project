
import pymysql

CONN = dict(
    host="127.0.0.1",
    port=3306,              # 3306 per your XAMPP screen
    user="root",            # or dev_user if you set it
    password="",            # "" for root on fresh XAMPP
    database="University",
    cursorclass=pymysql.cursors.DictCursor,
)

def main():
    conn = pymysql.connect(**CONN)
    with conn.cursor() as cur:
        cur.execute("SELECT DATABASE() AS db;")
        print("Connected to:", cur.fetchone()["db"])
        cur.execute("SHOW TABLES;")
        tables = [row[next(iter(row))] for row in cur.fetchall()]
        print("Tables found:", len(tables))
        print(sorted(tables))
    conn.close()

if __name__ == "__main__":
    main()
