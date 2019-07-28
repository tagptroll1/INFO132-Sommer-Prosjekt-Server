from app.site.api.ApiBase import (
    ApiBaseById, ApiBaseDefault, ApiBaseFilteredSet, ApiBaseSet
)
from app.site.models.fill_in import FillInModel


class FillIn(ApiBaseDefault):
    """/fill_in"""

    model = FillInModel


class FillInById(ApiBaseById):
    """/fill_in/<id>"""

    model = FillInModel


class FillInSet(ApiBaseSet):
    """/fill_in/set/<limit>"""

    model = FillInModel


class FillInFilteredSet(ApiBaseFilteredSet):
    """/fill_in/set/filter/<limit>"""

    model = FillInModel


endpoints = {
    "/fill_in": FillIn,
    "/fill_in/<id_>": FillInById,
    "/fill_in/set/<int:limit>": FillInSet,
    "/fill_in/set/filter/<int:limit>": FillInFilteredSet
}

__slots__ = [endpoints]