import typing

from .ApiBase import ApiBase, ApiBaseDefault, ApiBaseById, validate_body
from app.decorators.api_decorators import json_serialize
from app.decorators.protected import protected
from app.site.exceptions import QuestionAlreadyExistsException
from app.site.models.feedback import Feedback as FeedbackModel
from app.site.models.question_feedback import QuestionFeedback as QuestionFeedbackModel


from flask import request


class Feedback(ApiBaseDefault):
    model = FeedbackModel


class FeedbackById(ApiBase):
    @protected
    @json_serialize
    def delete(self, id_):
        delete_result = self.database.delete(FeedbackModel.TABLE, _id=id_)

        if delete_result.deleted_count:
            return {"message": "ok"}
        return {"message": "nothing deleted"}, 400

    @json_serialize
    def get(self, id_):
        getted = self.database.find_one(FeedbackModel.TABLE, feedback_id=id_)
        if getted:
            return getted, 200
        return self.database.find_one(FeedbackModel.TABLE, _id=id_)


class QuestionFeedback(ApiBase):
    @json_serialize
    def get(self):
        self.manager.log.info(
            f"All {QuestionFeedbackModel.TABLE} entires were requested."
        )
        return list(self.database.find(QuestionFeedbackModel.TABLE, question_id={"$exists": True}))

    @protected
    @json_serialize
    def post(self):
        body = request.get_json()

        types = typing.get_type_hints(QuestionFeedbackModel)
        error_or_None = validate_body(body, types)

        if error_or_None is not None:
            return error_or_None

        doesnt_exist = []
        for answer, feedback_id in body["feedbacks"].items():
            id_ = feedback_id
            if not self.database.exists(QuestionFeedbackModel.TABLE, feedback_id=id_):
                doesnt_exist.append(id_)

        if doesnt_exist:
            return {
                "message": f'[{", ".join(doesnt_exist)}] feedback ids dont exist'
            }, 400

        if not self.database.exists("questions", _id=body["question_id"]):
            return {"message": "Question does not exist"}, 400

        try:
            response = self.database.insert_one(
                QuestionFeedbackModel.TABLE, body
            )
        except QuestionAlreadyExistsException as e:
            self.manager.log.info(
                f"{QuestionFeedbackModel.TABLE} post returned 409 | {e}"
            )
            return {"message": str(e)}, 409
        except Exception as e:
            self.manager.log.info(
                f"{QuestionFeedbackModel.TABLE} post returned 500 | {e}"
            )
            return {"message": "Internal server error"}, 500

        self.manager.log.info(f"{QuestionFeedbackModel.TABLE} question was posted.")
        if response:
            return body, 201
        else:
            return {"message": "something went wrong"}, 500


class FeedbackSet(ApiBase):
    @json_serialize
    def post(self):
        body = request.get_json()
        feedbacks = list(self.database.find("feedback", question_id=body))
        response = []
        for feedback in feedbacks:
            q_feeds = feedback["feedbacks"]
            ids = list(q_feeds.values())
            q_feedbacks = list(self.database.find("feedback", feedback_id=ids))

            resp = {"question_id": feedback["question_id"]}
            for key, value in q_feeds.items():
                for feed in q_feedbacks:
                    if feed["feedback_id"] == value:
                        resp[key] = feed["feedback"]
            response.append(resp)

        return response


endpoints = {
    "/api/v1/feedback": Feedback,
    "/api/v1/feedback/<id_>": FeedbackById,
    "/api/v1/question_feedback": QuestionFeedback,
    "/api/v1/question_feedback/set": FeedbackSet,
}
