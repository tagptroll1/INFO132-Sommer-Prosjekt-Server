import random

from app.decorators.api_decorators import json_serialize
from app.site.exceptions import QuestionAlreadyExistsException

from flask import request

from flask_restful import Resource


class ApiBase(Resource):
    @classmethod
    def add(cls, manager, path):
        cls.manager = manager
        cls.database = manager.db
        manager.api.add_resource(cls, path)


class ApiBaseDefault(ApiBase):
    @json_serialize
    def get(self):
        self.manager.log.info(f"All {self.TABLE} questions were requested.")
        return list(self.database.find(self.TABLE))

    @json_serialize
    def post(self):
        body = request.get_json()

        try:
            response = self.database.insert_one(self.TABLE, body)
        except QuestionAlreadyExistsException as e:
            self.manager.log.info(f"{self.TABLE} post returned 409 | {e}")
            return {"message": e}, 409
        except Exception as e:
            self.manager.log.info(f"{self.TABLE} post returned 500 | {e}")
            return {"message": "Internal server error"}, 500

        self.manager.log.info(f"{self.TABLE} question was posted.")
        if response:
            return body, 201
        else:
            return {"message": "something went wrong"}, 500

    @json_serialize
    def delete(self):
        return {f"message": "Invalid request, use /{self.TABLE}/:id"}, 400

    @json_serialize
    def put(self):
        body = request.get_json()

        old_record = body.get("old")
        new_record = body.get("new")

        if not old_record:
            return {"message": "json body does not contain key `old`"}, 400

        if not new_record:
            return {"message": "json body does not contain key `new`"}, 400

        if not self.database.exists(self.TABLE, **old_record):
            return {"message": "Question does not exist"}, 400

        new_question = self.database.edit(self.TABLE, old_record, new_record)
        return new_question


class ApiBaseById(ApiBase):
    @json_serialize
    def delete(self, id_):
        delete_result = self.database.delete(self.TABLE, _id=id_)

        if delete_result.deleted_count:
            return {"message": "ok"}
        return {"message": "nothing deleted"}, 400

    @json_serialize
    def get(self, id_):
        return self.database.find_one(self.TABLE, _id=id_), 200


class ApiBaseSet(ApiBase):
    @json_serialize
    def get(self, limit):
        count = self.database.count(self.TABLE)
        if limit > count:
            return {"message": f"Limit too high, max is: {count}"}, 400

        all_entries = list(self.database.find(self.TABLE))
        random.shuffle(all_entries)

        return all_entries[:limit], 200


class ApiBaseFilteredSet(ApiBase):
    @json_serialize
    def get(self, limit):
        args = request.args

        count = self.database.count(self.TABLE)
        if limit > count:
            return {"message": f"Limit too high, max is: {count}"}, 400

        # assuming args is a dict, convert later if needed !TODO look into
        assert isinstance(args, dict)

        all_entries = list(self.database.find(self.TABLE, **args))
        random.shuffle(all_entries)

        return all_entries[:limit], 200
