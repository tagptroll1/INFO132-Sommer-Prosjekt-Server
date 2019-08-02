from app.site.api.ApiBase import (
    ApiBaseById, ApiBaseDefault, ApiBaseSet
)
from app.site.models.multi_choice import MultiChoiceModel


class MultiChoice(ApiBaseDefault):
    """/multi_choice"""

    model = MultiChoiceModel


class MultiChoiceById(ApiBaseById):
    """/multi_choice/<id>"""

    model = MultiChoiceModel


class MultiChoiceSet(ApiBaseSet):
    """/multi_choice/set/<limit>"""

    model = MultiChoiceModel


endpoints = {
    "/api/v1/multi_choice": MultiChoice,
    "/api/v1/multi_choice/<id_>": MultiChoiceById,
    "/api/v1/multi_choice/set/<int:limit>": MultiChoiceSet,
}

__slots__ = [endpoints]