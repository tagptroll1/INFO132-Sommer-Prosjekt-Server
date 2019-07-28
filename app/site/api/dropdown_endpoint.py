from app.site.api.ApiBase import (
    ApiBaseById, ApiBaseDefault, ApiBaseFilteredSet, ApiBaseSet
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


class DropdownFilteredSet(ApiBaseFilteredSet):
    """/dropdown/set/filter/<limit>"""

    model = DropdownModel


endpoints = {
    "/dropdown": Dropdown,
    "/dropdown/<id_>": DropdownById,
    "/dropdown/set/<int:limit>": DropdownSet,
    "/dropdown/set/filter/<int:limit>": DropdownFilteredSet
}

__slots__ = [endpoints]