from app.site.models.session_data import DataModel

from .ApiBase import ApiBaseDefault


class DataEndpoint(ApiBaseDefault):
    """/api/v1/data"""

    model = DataModel


endpoints = {
    "/api/v1/data": DataEndpoint
}

__slots__ = [endpoints]
