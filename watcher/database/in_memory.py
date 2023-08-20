import pandas as pd
import os


class InMemoryDB:
    """
    InMemoryDB is a class that represents a database in memory.
    """

    def __init__(self, db_file_path: str):
        self.data = pd.DataFrame()
        self.db_file_path = db_file_path
        if db_file_path:
            if os.path.isfile(db_file_path):
                self.data = pd.read_json(db_file_path)

    def insert(self, data: pd.DataFrame):
        """
        Insert data into the database.
        """
        self.data = pd.concat([self.data, data], ignore_index=True)
        if self.db_file_path:
            self.data.to_json(self.db_file_path, mode="w")

    def delete(self, link: str):
        """
        Delete data from the database based on the link.
        """
        self.data = self.data.drop(self.data[self.data.link == link].index)

    def query(self, query: str):
        """
        Query the database based on the query.
        """
        return self.data.query(query)

    def get(self):
        """
        get the data from the database.
        """
        return self.data
