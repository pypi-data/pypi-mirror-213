from sqlitedict import SqliteDict


class IPDataManipulation:
    @staticmethod
    def save_data(f):
        def wrapper(*args):
            db = SqliteDict(args[-1], autocommit=True)
            if db.get("node"):
                node = db["node"]
                args = (args[0], node, args[2], args[3], args[4])
                f(*args)
                db["node"] = node
            else:
                f(*args)
                db["node"] = args[1]
            db.close()

        return wrapper

    @staticmethod
    def remove_data(f):
        def wrapper(*args):
            db = SqliteDict(args[-1], autocommit=True)
            f(*args)
            db["node"] = args[0].head
            db.close()

        return wrapper

    @staticmethod
    def save_updated_data(f):
        def wrapper(*args):
            db = SqliteDict(args[-1], autocommit=True)
            if db.get("node"):
                node = db["node"]
                args = (args[0], node, args[2], args[3])
                f(*args)
                db["node"] = node
                db.close()

        return wrapper

    @staticmethod
    def access_data(f):
        def wrapper(*args):
            db = SqliteDict(args[-1], autocommit=True)
            if db.get("node"):
                node = db["node"]
                args = (args[0], node, args[2], args[3])
                result = f(*args)
                db.close()
                return result
            db.close()
            return None

        return wrapper
