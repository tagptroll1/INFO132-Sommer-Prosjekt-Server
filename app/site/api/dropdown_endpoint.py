from app.site.api.ApiBase import (
    ApiBaseById, ApiBaseDefault, ApiBaseSet
)
from app.site.models.dropdown import DropdownModel


class Dropdown(ApiBaseDefault):
    """/dropdown"""

    model = DropdownModel


class DropdownById(ApiBaseById):
    """/dropdown/<id>"""

    model = DropdownModel


class DropdownSet(ApiBaseSet):
    """/dropdown/set/<limit>"""

    model = DropdownModel

endpoints = {
    "/api/v1/dropdown": Dropdown,
    "/api/v1/dropdown/<id_>": DropdownById,
    "/api/v1/dropdown/set/<int:limit>": DropdownSet,
    "/api/v1/dropdown/set/filter/<int:limit>": DropdownFilteredSet
}

__slots__ = [endpoints]