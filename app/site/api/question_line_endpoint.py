from app.site.api.ApiBase import (
    ApiBaseById, ApiBaseDefault, ApiBaseSet
)
from app.site.models.question_line import QuestionLineModel


class QuestionLine(ApiBaseDefault):
    """/questionline"""

    model = QuestionLineModel


class QuestionLineById(ApiBaseById):
    """/questionline/<id>"""

    model = QuestionLineModel


class QuestionLineSet(ApiBaseSet):
    """/questionline/set/<limit>"""

    model = QuestionLineModel


endpoints = {
    "/api/v1/questionline": QuestionLine,
    "/api/v1/questionline/<id_>": QuestionLineById,
    "/api/v1/questionline/set/<int:limit>": QuestionLineSet,
}