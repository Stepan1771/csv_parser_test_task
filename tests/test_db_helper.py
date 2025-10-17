import unittest
import os
from script.db_helper import DataBaseHelper


class TestDataBaseHelper(unittest.TestCase):

    def setUp(self):
        # Удаляем базу данных, если она существует
        if os.path.exists("test_database.db"):
            os.remove("test_database.db")
        self.db = DataBaseHelper(url="test_database.db")


    def tearDown(self):
        # Закрываем соединение и удаляем файл базы данных
        self.db.close()
        if os.path.exists("test_database.db"):
            os.remove("test_database.db")

    def test_create_table(self):
        response = self.db.create_table()
        self.assertEqual(response["status"], "Created table 'data'")
        self.db.cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='data'")
        table = self.db.cur.fetchone()
        self.assertIsNotNone(table)

    def test_insert_data_and_average_rating(self):
        self.db.create_table()
        headers = ("name", "brand", "price", "rating")
        row = ["Product1", "BrandA", "100", "4.5"]
        self.db.insert_data(headers, row)
        self.db.cur.execute("SELECT * FROM data")
        data = self.db.cur.fetchall()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0][1], "BrandA")  # бренд

        row2 = ["Product2", "BrandA", "200", "3.5"]
        self.db.insert_data(headers, row2)

        result = self.db.average_rating()
        self.assertTrue(any(r[0] == "BrandA" and abs(r[1] - 4.0) < 0.01 for r in result))

    def test_drop_db(self):
        self.db.create_table()
        response = self.db.drop_db()
        self.assertEqual(response["status"], "Dropped table 'data'")
        self.db.cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='data'")
        table = self.db.cur.fetchone()
        self.assertIsNone(table)

if __name__ == '__main__':
    unittest.main()