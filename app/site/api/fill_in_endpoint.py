from app.site.api.ApiBase import (
    ApiBaseById, ApiBaseDefault, ApiBaseSet
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
}

__slots__ = [endpoints]