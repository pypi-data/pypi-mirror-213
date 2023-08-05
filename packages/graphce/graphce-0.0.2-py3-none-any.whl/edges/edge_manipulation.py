# python level imports
import sqlitedict

class Edge:
    def __init__(self, edge_location: str):
        self._edge_location = edge_location
        self.db = sqlitedict.SqliteDict(edge_location, autocommit=True)

    def _create_edge(self, key: tuple, value: str) -> None:
        self.db[str(key)] = value
        return

    def _access_edge(self, key: tuple) -> str:
        if str(key) in self.db:
            value = self.db[str(key)]
        else:
            raise ValueError('Key not found')
        self.db.close()
        return value

    def _update_edge(self, key: tuple, value:str) -> None:

        if str(key) in self.db:
            self.db[str(key)] = value
        else:
            raise ValueError('Key not found')
        self.db.close()
        return

    def _delete_edge(self, key: str):

        if str(key) in self.db:
            del self.db[str(key)]
        else:
            raise ValueError('Key not found')
        return