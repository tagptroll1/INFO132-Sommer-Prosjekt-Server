import logging

from flask_restful import Api

from .database import MongoDb


class Manager:
    def __init__(self, app):
        self.app = app
        self.api = Api(self.app)
        self.db = MongoDb()
        self.log = logging.getLogger(__name__)

        self.log.debug("Manager initialized")

    def add_from_dict(self, dic):
        for endpoint, class_ in dic.items():
            class_.add(self, endpoint)

    def load_api_resources(self, endpoints):
        for endpoint in endpoints:
            self.add_from_dict(endpoint)

    def run(self, debug):
        self.app.run(debug=debug)


