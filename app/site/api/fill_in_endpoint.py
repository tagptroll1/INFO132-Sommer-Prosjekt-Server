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


endpoints = {
    "/api/v1/fill_in": FillIn,
    "/api/v1/fill_in/<id_>": FillInById,
    "/api/v1/fill_in/set/<int:limit>": FillInSet,
    "/api/v1/fill_in/set/filter/<int:limit>": FillInFilteredSet
}

__slots__ = [endpoints]