import os

from bson.objectid import ObjectId

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

    def delete(self, table_name: str) -> dict:
        ...

    def drop_table(self, table_name):
        ...

    def filter(self, table_name, predicate):
        ...

    def get(self, table_name, key):
        table = getattr(self.db, table_name)

    def get_all(self, table_name, *keys):
        ...

    def insert(self, table_name, *objects):
        if not objects:
            return

        table = getattr(self.db, table_name)

        if len(objects) == 1:
            table.insert_one(objects[0])

        else:
            table.insert_many(objects)

        return True

    def map(self, table_name, func):
        ...
