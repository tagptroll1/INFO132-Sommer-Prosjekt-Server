from app.site.api.ApiBase import (
    ApiBaseById, ApiBaseDefault, ApiBaseFilteredSet, ApiBaseSet
)


class Dropdown(ApiBaseDefault):
    TABLE = "dropdown"


class DropdownById(ApiBaseById):
    TABLE = "dropdown"


class DropdownSet(ApiBaseSet):
    TABLE = "dropdown"


class DropdownFilteredSet(ApiBaseFilteredSet):
    TABLE = "dropdown"
