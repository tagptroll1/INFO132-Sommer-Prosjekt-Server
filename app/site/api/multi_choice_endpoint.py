from app.site.api.ApiBase import (
    ApiBaseById, ApiBaseDefault, ApiBaseFilteredSet, ApiBaseSet
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
    "/api/v1/multi_choice/set/filter/<int:limit>": MultiChoiceFilteredSet
}

__slots__ = [endpoints]