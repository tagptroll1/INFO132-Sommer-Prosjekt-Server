from app.site.models.session_data import DataModel

from .ApiBase import ApiBaseDefault


class DataEndpoint(ApiBaseDefault):
    """/data"""

    model = DataModel


endpoints = {
    "/data": DataEndpoint
}

__slots__ = [endpoints]
