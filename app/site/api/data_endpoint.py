import typing

from app.decorators.api_decorators import json_serialize
from app.decorators.protected import protected
from app.site.api.ApiBase import ApiBase, ApiBaseDefault, validate_body
from app.site.exceptions import QuestionAlreadyExistsException
from app.site.models.session_data import DataModel

from flask import request


class DataEndpoint(ApiBaseDefault):
    """/api/v1/data"""

    model = DataModel


class DatasetEndpoint(ApiBase):
    """/api/v1/dataset"""
    @protected
    @json_serialize
    def post(self):
        table = DataModel.TABLE
        body = request.get_json()


        if not isinstance(body, list):
            return {"message": "body must be a list"}, 400

        response = []

        for entry in body:
            types = typing.get_type_hints(DataModel)
            error_or_None = validate_body(entry, types)
            if error_or_None is not None:
                return error_or_None

            try:
                resp = self.database.insert_one(table, entry)
                response.append(resp)
            except QuestionAlreadyExistsException as e:
                self.manager.log.info(
                    f"{table} post returned 409 | {e}"
                )
                response.append(
                    {"message": f"entry already exists",
                    "entry": entry}
                )
            except Exception as e:
                self.manager.log.info(
                    f"{table} post returned 500 | {e}"
                )
                return {"message": "Internal server error"}, 500

            self.manager.log.info(f"{table} dataentry was posted.")
        return response

    @protected
    @json_serialize
    def delete(self):
        self.database.drop_table(DataModel.TABLE)

        
endpoints = {
    "/api/v1/data": DataEndpoint,
    "/api/v1/dataset": DatasetEndpoint
}

__slots__ = [endpoints]
