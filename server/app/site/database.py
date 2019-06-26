import os

from pymongo import MongoClient


TABLES = [
    "multi_choice",
    "dropdown",
    "codesnippet",
    "tracking",
    "feedback"
]


class MongoDb(object):
    def __init__(self):
        self.host = os.environ.get("MONGO_HOST")
        if self.host is None:
            self.host = "127.0.0.1"

        self.port = os.environ.get("MONGO_PORT")
        if self.port is None:
            self.port = "28015"

        self.database = os.environ.get("MONGO_DATABASE")
        if self.database is None:
            self.database = "slangeuib"

        self.client = MongoClient(f"mongodb://{self.host}:{self.port}/")
        self.db = self.client[self.database]

    def __getattribute__(self, attr):
        method = object.__getattribute__(self, attr)

        def wrapper(callble):
            def func(table_name, *args, **kwargs):
                if table_name in TABLES:
                    callble(table_name, *args, **kwargs)
                else:
                    raise UserWarning(f"Table '{table_name}' is not allowed")
            return func

        if callable(method):
            return wrapper(method)

        return method

    def delete(self, table_name: str, **kwargs) -> dict:
        print(self.db.slangeuib)
        table = self.db[table_name]
        return table.delete_one(**kwargs)        

    def delete_many(self, table_name: str, **kwargs) -> dict:
        table = getattr(self.db, table_name)
        return table.delete_many(**kwargs)

    def drop_table(self, table_name):
        try:
            self.db.drop_collection(table_name)
        except:
            return False
        return True

    def filter(self, table_name, predicate):
        ...


    def find_one(self, table_name, **kwargs):
        table = getattr(self.db, table_name)
        return table.find_one(kwargs)

    def find(self, table_name, **kwargs):
        table = getattr(self.db, table_name)
        return table.find(**kwargs)

    def insert(self, table_name, *objects):
        if not objects:
            return

        table = getattr(self.db, table_name)

        if len(objects) == 1:
            return [table.insert_one(objects[0])]

        return table.insert_many(objects)


    def map(self, table_name, func, **kwargs):
        files = self.find(**kwargs)
        return map()

    def count(self, table_name, **kwargs):
        if kwargs:
            return self.find(**kwargs).count()
            
        return getattr(self.db, table_name).count()
