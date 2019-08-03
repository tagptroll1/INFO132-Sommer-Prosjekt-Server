import random
import typing
from typing import Optional

from app.decorators.api_decorators import json_serialize
from app.site.exceptions import QuestionAlreadyExistsException

from flask import request

from flask_restful import Resource

def convert_args_value(types, args):
    new_args = {}
    for key, value in args.items():
        type_ = types[key]

        # The value is already a str, so don't have to check that
        if type_ is int or type_ is bool: 
            new_args[key] = types[key](value)
        # Seperate value by commas if it's a list.
        elif "," in value:
            new_args[key] = value.split(",")
        else:
            new_args[key] = value

    return new_args

def validate_body(body, types, post=True):
    for var, type_ in types.items():
        if post and type_ != Optional and var not in body:
            return {"message": f"{var} is a required field!"}, 400

        for key, value in body.items():
            if var == key and type_ != Optional and not isinstance(value, type_):
                return {
                    "message": (
                        f"{var} must be of type {type_} not {type(value)}"
                    )
                }, 400

            if key not in types:
                return {
                    "message": f"{key} is not a supported field"
                }, 400


class ApiBase(Resource):
    @classmethod
    def add(cls, manager, path):
        cls.manager = manager
        cls.database = manager.db
        manager.api.add_resource(cls, path)


class ApiBaseDefault(ApiBase):
    @json_serialize
    def get(self):
        self.manager.log.info(
            f"All {self.model.TABLE} questions were requested."
        )
        return list(self.database.find(self.model.TABLE))

    @json_serialize
    def post(self):
        body = request.get_json()

        types = typing.get_type_hints(self.model)
        error_or_None = validate_body(body, types)

        if error_or_None is not None:
            return error_or_None

        body["type"] = self.model.TABLE

        try:
            response = self.database.insert_one(
                self.model.TABLE, body
            )
        except QuestionAlreadyExistsException as e:
            self.manager.log.info(
                f"{self.model.TABLE} post returned 409 | {e}"
            )
            return {"message": str(e)}, 409
        except Exception as e:
            self.manager.log.info(
                f"{self.model.TABLE} post returned 500 | {e}"
            )
            return {"message": "Internal server error"}, 500

        self.manager.log.info(f"{self.model.TABLE} question was posted.")
        if response:
            return body, 201
        else:
            return {"message": "something went wrong"}, 500

    @json_serialize
    def delete(self):
        return {
            "message": f"Invalid request, use /{self.model.TABLE}/:id"
        }, 400

    @json_serialize
    def put(self):
        body = request.get_json()

        types = typing.get_type_hints(self.model)
        error_or_None = validate_body(
            body.get("new", []), types, post=False
        )

        if error_or_None is not None:
            return error_or_None

        old_record = body.get("old")
        new_record = body.get("new")

        if not old_record:
            return {"message": "json body does not contain key `old`"}, 400

        if not new_record:
            return {"message": "json body does not contain key `new`"}, 400

        if not self.database.exists(self.model.TABLE, **old_record):
            return {"message": "Question does not exist"}, 400

        new_question = self.database.edit(
            self.model.TABLE, old_record, new_record
        )
        return new_question


class ApiBaseById(ApiBase):
    @json_serialize
    def delete(self, id_):
        delete_result = self.database.delete(self.model.TABLE, _id=id_)

        if delete_result.deleted_count:
            return {"message": "ok"}
        return {"message": "nothing deleted"}, 400

    @json_serialize
    def get(self, id_):
        return self.database.find_one(self.model.TABLE, _id=id_), 200


class ApiBaseSet(ApiBase):
    @json_serialize
    def get(self, limit):
        args = dict(request.args)
        types = typing.get_type_hints(self.model)

        args = convert_args_value(types, args)
        print(args)
        count = self.database.count(self.model.TABLE)
        if limit > count:
            return {"message": f"Limit too high, max is: {count}"}, 400

        all_entries = list(self.database.find(self.model.TABLE, **args))
        random.shuffle(all_entries)

        return all_entries[:limit], 200
