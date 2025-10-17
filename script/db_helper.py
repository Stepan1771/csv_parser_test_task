import sqlite3


class DataBaseHelper:
    def __init__(
            self,
            url: str = "database.db",
    ):
        self.con = sqlite3.connect(url)
        self.cur = self.con.cursor()


    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS data(name, brand, price, rating)
        """)
        self.con.commit()
        return {
            "status": "Created table 'data'",
        }

    def insert_data(
            self,
            headers: tuple,
            row: list,
    ):
        placeholders = ", ".join(["?" for _ in headers])
        columns = ", ".join([f'"{header}"' for header in headers])

        stmt = f"INSERT INTO data ({columns}) VALUES ({placeholders})"
        self.cur.execute(stmt, row)
        self.con.commit()

        return {
            "status": "Inserted data",
        }

    def average_rating(self):
        self.cur.execute("""
            SELECT brand, AVG(rating) AS rating 
            FROM data
            GROUP BY brand
            ORDER BY rating DESC
            """)
        result = self.cur.fetchall()
        return result

    def drop_db(self):
        self.cur.execute("""
            DROP TABLE data
        """)
        self.con.commit()

        return {
            "status": "Dropped table 'data'",
        }

    def close(self):
        self.con.close()


db_helper = DataBaseHelper()
