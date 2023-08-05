"""

"""
# Python level imports
import sqlitedict
from sqlitedict import SqliteDict

class DB_Creation:
    def __init__(self, location: str, edge_location: str):
        """
        :param location: path of database as a string
        """
        self._create_database(location)
        self._create_edge_db(edge_location)

    def _create_database(self, location: str) -> SqliteDict:
        db = sqlitedict.SqliteDict(location)
        return db

    def _create_edge_db(self, location: str) -> SqliteDict:
        db = sqlitedict.SqliteDict(location)
        return db

