import pandas as pd

class InMemoryDB:
    """
    InMemoryDB is a class that represents a database in memory.
    """
    def __init__(self):
        self.data = pd.DataFrame()

    def insert(self, data: pd.DataFrame):
        """
        Insert data into the database.
        """
        self.data = pd.concat([self.data, data], ignore_index=True)

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
