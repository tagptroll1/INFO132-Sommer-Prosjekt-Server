import logging

from flask import Flask

from flask_restful import Api

from .api.dropdown_endpoint import (
    Dropdown, DropdownById, DropdownFilteredSet, DropdownSet
)
from .api.multi_choice_endpoint import (
    MultiChoice, MultiChoiceById, MultiChoiceFilteredSet, MultiChoiceSet
)
from .database import MongoDb


class Manager:
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.db = MongoDb()
        self.log = logging.getLogger(__name__)

        self.log.debug("Manager initialized")

    def load_api_resources(self):
        Dropdown.add(self, "/dropdown")
        DropdownById.add(self, "/dropdown/<id_>")
        DropdownSet.add(self, "/dropdown/set/<int:limit>")
        DropdownFilteredSet.add(self, "/dropdown/set/filter/<int:limit>")

        MultiChoice.add(self, "/multi_choice")
        MultiChoiceById.add(self, "/multi_choice/<id_>")
        MultiChoiceSet.add(self, "/multi_choice/set/<int:limit>")
        MultiChoiceFilteredSet.add(
            self, "/multi_choice/set/filter/<int:limit>")

    def run(self):
        self.app.run(debug=True)
