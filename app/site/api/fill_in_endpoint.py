from app.site.api.ApiBase import (
    ApiBaseById, ApiBaseDefault, ApiBaseSet
)
from app.site.models.fill_in import FillInModel


class FillIn(ApiBaseDefault):
    """/fillin"""

    model = FillInModel


class FillInById(ApiBaseById):
    """/fillin/<id>"""

    model = FillInModel


class FillInSet(ApiBaseSet):
    """/fillin/set/<limit>"""

    model = FillInModel


endpoints = {
    "/api/v1/fillin": FillIn,
    "/api/v1/fillin/<id_>": FillInById,
    "/api/v1/fillin/set/<int:limit>": FillInSet,
}

__slots__ = [endpoints]