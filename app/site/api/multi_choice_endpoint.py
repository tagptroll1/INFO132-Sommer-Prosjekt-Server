from app.site.api.ApiBase import (
    ApiBaseById, ApiBaseDefault, ApiBaseSet
)
from app.site.models.multi_choice import MultiChoiceModel


class MultiChoice(ApiBaseDefault):
    """/multichoice"""

    model = MultiChoiceModel


class MultiChoiceById(ApiBaseById):
    """/multichoice/<id>"""

    model = MultiChoiceModel


class MultiChoiceSet(ApiBaseSet):
    """/multichoice/set/<limit>"""

    model = MultiChoiceModel


endpoints = {
    "/api/v1/multichoice": MultiChoice,
    "/api/v1/multichoice/<id_>": MultiChoiceById,
    "/api/v1/multichoice/set/<int:limit>": MultiChoiceSet,
}

__slots__ = [endpoints]