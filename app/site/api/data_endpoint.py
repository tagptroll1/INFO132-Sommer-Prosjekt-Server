import os
import typing

from app.decorators.api_decorators import json_serialize
from app.decorators.protected import protected
from app.site.api.ApiBase import ApiBase, ApiBaseDefault, validate_body
from app.site.exceptions import QuestionAlreadyExistsException
from app.site.models.session_data import DataModel, QuestionDataModel

from flask import request


class DataEndpoint(ApiBaseDefault):
    """/api/v1/data"""

    model = DataModel


class DatasetEndpoint(ApiBase):
    """/api/v1/dataset"""
    @protected
    @json_serialize
    def post(self):
        body = request.get_json()

        types = typing.get_type_hints(DataModel)
        error_or_None = validate_body(body, types)
        if error_or_None is not None:
            return {
                "message": f"{error_or_None} - body invalid"
            }, 400

        # Validate questions
        types = typing.get_type_hints(QuestionDataModel)
        questions = body["questions"]
        errors = []
        for question in questions:
            error_or_None = validate_body(question, types)
            if error_or_None is not None:
                errors.append({
                    "message": f"{error_or_None} - question invalid"
                })

        if errors:
            return {"error": errors}, 400

        try:
            resp = self.database.insert_one(DataModel.TABLE, body)
        except QuestionAlreadyExistsException as e:
            self.manager.log.info(
                f"{DataModel.TABLE} post returned 409 | {e}"
            )
            return {"message": f"entry already exists"}, 400

        except Exception as e:
            self.manager.log.info(
                f"{DataModel.TABLE} post returned 500 | {e}"
            )
            if os.environ.get("env") == "production":
                return {"message": "Internal server error"}, 500
            else:
                return {
                    "message": "Internal server error",
                    "error": str(e)
                }, 500
        self.manager.log.info(f"{DataModel.TABLE} dataentry was posted.")

        return resp

    @protected
    @json_serialize
    def delete(self):
        self.database.drop_table(DataModel.TABLE)


endpoints = {
    "/api/v1/data": DataEndpoint,
    "/api/v1/dataset": DatasetEndpoint
}

__slots__ = [endpoints]
