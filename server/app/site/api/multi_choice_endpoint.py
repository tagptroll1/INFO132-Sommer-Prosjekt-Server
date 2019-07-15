from app.site.api.ApiBase import (
    ApiBaseById, ApiBaseDefault, ApiBaseFilteredSet, ApiBaseSet
)


class MultiChoice(ApiBaseDefault):
    """/multi_choice"""

    TABLE = "multi_choice"


class MultiChoiceById(ApiBaseById):
    """/multi_choice/<id>"""

    TABLE = "multi_choice"


class MultiChoiceSet(ApiBaseSet):
    """/multi_choice/set/<limit>"""

    TABLE = "multi_choice"


class MultiChoiceFilteredSet(ApiBaseFilteredSet):
    """/multi_choice/set/filter/<limit>"""

    TABLE = "multi_choice"
