import typing

from .ApiBase import ApiBase, ApiBaseDefault, ApiBaseById, validate_body
from app.decorators.api_decorators import json_serialize
from app.decorators.protected import protected
from app.site.exceptions import QuestionAlreadyExistsException
from app.site.models.feedback import Feedback


from flask import request


class Feedback(ApiBaseDefault):
    model = Feedback


class FeedbackById(ApiBaseById):
    model = Feedback


class QuestionFeedback(ApiBase):
    model = Feedback

    @json_serialize
    def get(self):
        self.manager.log.info(
            f"All {self.model.TABLE} entires were requested."
        )
        return list(self.database.find(self.model.TABLE))

    @protected
    @json_serialize
    def post(self):
        body = request.get_json()

        types = typing.get_type_hints(self.model)
        error_or_None = validate_body(body, types)

        if error_or_None is not None:
            return error_or_None

        body["type"] = self.model.TABLE

        doesnt_exist = []
        for feedback in body["feedbacks"]:
            id_ = feedback["feedback_id"]
            if not self.database.exists("feedback", feedback_id=id_):
                doesnt_exist.append(id_)

        if doesnt_exist:
            return {
                "message": f'{", ".join(doesnt_exist)} feedback ids dont exist'
            }, 400

        if not self.database.exists(body["question_id"]):
            ...

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


class FeedbackSet(ApiBase):
    @json_serialize
    def post(self):
        body = request.get_json()
