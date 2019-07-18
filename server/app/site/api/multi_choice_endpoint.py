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


class MultiChoiceFilteredSet(ApiBaseFilteredSet):
    """/multi_choice/set/filter/<limit>"""

    model = MultiChoiceModel
