from app.site.api.ApiBase import (
    ApiBaseById, ApiBaseDefault, ApiBaseFilteredSet, ApiBaseSet
)
from app.site.models.dropdown import DropdownModel


class Dropdown(ApiBaseDefault):
    model = DropdownModel


class DropdownById(ApiBaseById):
    model = DropdownModel


class DropdownSet(ApiBaseSet):
    model = DropdownModel


class DropdownFilteredSet(ApiBaseFilteredSet):
    model = DropdownModel
