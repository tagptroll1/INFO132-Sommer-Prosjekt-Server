import random

from app.decorators.api_decorators import json_serialize
from app.site.api.ApiBase import ApiBase
from app.site.exceptions import QuestionAlreadyExistsException

from flask import request


class MultiChoice(ApiBase):
    """/multichoice"""

    TABLE = "multi_choice"

    @json_serialize
    def get(self):
        self.manager.log.info("All multichoice questions were requested.")
        return list(self.manager.db.find(self.TABLE))

    @json_serialize
    def post(self):
        body = request.get_json()

        try:
            response = self.manager.db.insert_one(self.TABLE, body)
        except QuestionAlreadyExistsException as e:
            print(e)
            return {"message": e}, 409
        except Exception as e:
            print(e)
            return {"message": "Internal server error"}, 500

        self.manager.log.info("Multichoice question was posted.")
        if response:
            return body, 201
        else:
            return {"message": "something went wrong"}, 500

    def delete(self):
        return {"message": "Invalid request, use /multichoice/:id"}, 400

    @json_serialize
    def put(self):
        body = request.get_json()

        old_record = body.get("old")
        new_record = body.get("new")

        if not old_record:
            return {"message": "json body does not contain key `old`"}, 400

        if not new_record:
            return {"message": "json body does not contain key `new`"}, 400

        if not self.manager.db.exists(self.TABLE, **old_record):
            return {"message": "Question does not exist"}, 400

        new_question = self.manager.db.edit(self.TABLE, old_record, new_record)
        return new_question


class MultiChoiceById(ApiBase):
    """/multichoice/<id>"""

    TABLE = "multi_choice"

    def delete(self, id_):
        delete_result = self.manager.db.delete(self.TABLE, _id=id_)

        if delete_result.deleted_count:
            return {"message": "ok"}
        return {"message": "nothing deleted"}, 400

    @json_serialize
    def get(self, id_):
        return self.manager.db.find_one(self.TABLE, _id=id_), 200


class MultiChoiceSet(ApiBase):
    """/multichoice/set/<limit>"""

    TABLE = "multi_choice"

    @json_serialize
    def get(self, limit):
        count = self.manager.db.count(self.TABLE)
        if limit > count:
            return {"message": f"Limit too high, max is: {count}"}, 400

        all_entries = list(self.manager.db.find(self.TABLE))
        random.shuffle(all_entries)

        return all_entries[:limit], 200


class MultiChoiceFilteredSet(ApiBase):
    """/multichoice/set/filter/<limit>"""

    TABLE = "multi_choice"

    @json_serialize
    def get(self, limit):
        args = request.args

        count = self.manager.db.count(self.TABLE)
        if limit > count:
            return {"message": f"Limit too high, max is: {count}"}, 400

        # assuming args is a dict, convert later if needed !TODO look into
        assert isinstance(args, dict)

        all_entries = list(self.manager.db.find(self.TABLE, **args))
        random.shuffle(all_entries)

        return all_entries[:limit], 200
