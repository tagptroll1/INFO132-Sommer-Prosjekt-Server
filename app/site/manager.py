import logging

from flask import Flask

from flask_restful import Api

from .database import MongoDb


class Manager(Flask):
    def __init__(self):
        super().__init__(__name__)
        self.api = Api(self)
        self.db = MongoDb()
        self.log = logging.getLogger(__name__)

        self.log.debug("Manager initialized")

    def add_from_dict(self, dic):
        for endpoint, class_ in dic.items():
            class_.add(self, endpoint)

    def load_api_resources(self, endpoints):
        for endpoint in endpoints:
            self.add_from_dict(endpoint)
