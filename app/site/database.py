import os

from app.decorators.database_decorators import convert_id
from app.site.exceptions import QuestionAlreadyExistsException

from bson.objectid import ObjectId

from pymongo import MongoClient


def get_query(kwargs):
    query = {}
    for key, value in kwargs.items():
        if isinstance(value, list):
            query[key] = {"$in": value}
        else:
            query[key] = {"$in": [value]}
    return query


class MongoDb(object):
    def __init__(self):
        self.host = os.environ.get("MONGO_HOST")
        if self.host is None:
            self.host = "localhost"

        self.port = os.environ.get("MONGO_PORT")
        if self.port is None:
            self.port = "27017"

        self.database = os.environ.get("MONGO_DATABASE")
        if self.database is None:
            self.database = "slangeuib"

        self.client = MongoClient(f"mongodb://{self.host}:{self.port}/")
        self.db = self.client[self.database]

    @convert_id
    def delete(self, table_name: str, **kwargs) -> dict:
        table = self.db[table_name]
        return table.delete_one(get_query(kwargs))

    @convert_id
    def delete_many(self, table_name: str, **kwargs) -> dict:
        table = self.db[table_name]
        return table.delete_many(get_query(kwargs))

    def drop_table(self, table_name):
        try:
            self.db.drop_collection(table_name)
        except Exception:
            return False
        return True

    def filter(self, table_name, predicate):
        ...

    @convert_id
    def find_one(self, table_name, **kwargs):
        table = self.db[table_name]
        return table.find_one(get_query(kwargs))

    @convert_id
    def find(self, table_name, **kwargs):
        table = self.db[table_name]
        return table.find(get_query(kwargs))


    def insert_one(self, table_name, obj):
        table = self.db[table_name]

        if self.find_one(table_name, **obj):
            raise QuestionAlreadyExistsException(
                "Question already exists.")

        _id = table.insert_one(obj).inserted_id
        obj["_id"] = _id

        return obj

    def edit(self, table_name, old, new, type_=None):
        table = self.db[table_name]
        if old.get("_id"):
            old["_id"] = ObjectId(old["_id"])

        if type_:
            old["type"] = type_

        table.update_one(old, {"$set": new})

        old.update(new)
        new_updated = self.find_one(table_name, **old)
        return new_updated

    def exists(self, table_name, **kwargs):
        return self.count(table_name, **kwargs) > 0

    def map(self, table_name, func, **kwargs):
        ...

    def count(self, table_name, **kwargs):
        if kwargs:
            return self.find(table_name, **kwargs).count()

        return self.db[table_name].count()
