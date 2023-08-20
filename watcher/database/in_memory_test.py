import unittest
from in_memory import InMemoryDB
import pandas as pd
import numpy as np


class TestInMemoryDB(unittest.TestCase):
    def setUp(self):
        self.db = InMemoryDB()

    def test_insert(self):
        insert_data = pd.DataFrame(
            data={
                "link": ["https://www.google.com"],
                "text": ["i hate unittest"],
                "start": [0],
                "end": [10],
                "embedding": [[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]],
            }
        )
        self.db.insert(insert_data)
        self.assertTrue(pd.DataFrame.equals(insert_data, self.db.get()))

    def test_delete(self):
        data1 = pd.DataFrame(
            data={
                "link": ["https://www.google.com"],
                "text": ["i hate unittest"],
                "start": [0],
                "end": [10],
                "embedding": [[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]],
            }
        )
        self.db.insert(data1)
        self.assertTrue(pd.DataFrame.equals(data1, self.db.get()))

        data2 = pd.DataFrame(
            data={
                "link": ["example.com"],
                "text": ["i hate unittest"],
                "start": [0],
                "end": [10],
                "embedding": [[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]],
            }
        )
        self.db.insert(data2)
        self.assertTrue(
            pd.DataFrame.equals(
                pd.concat([data1, data2], ignore_index=True), self.db.get()
            )
        )

        self.db.delete("example.com")
        self.assertTrue(pd.DataFrame.equals(data1, self.db.get()))


if __name__ == "__main__":
    unittest.main()
