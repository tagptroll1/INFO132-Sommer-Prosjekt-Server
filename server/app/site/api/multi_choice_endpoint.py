from app.decorators.api_decorators import json_serialize
from app.site.api.ApiBase import ApiBase

from flask import request


class MultiChoice(ApiBase):
    TABLE = "multi_choice"

    @json_serialize
    def get(self):
        self.manager.log.info("All multichoice questions were requested.")
        return list(self.manager.db.find(self.TABLE))

    @json_serialize
    def post(self):
        body = request.get_json()
        exists = False

        if self.manager.db.count(self.TABLE) > 0:
            exists = self.manager.db.find(self.TABLE, **body)

        if exists:
            return {"message": "Already exists"}, 409

        response = self.manager.db.insert(self.TABLE, body)

        self.manager.log.info("Multichoice question was posted.")
        if response:
            return body, 201
        else:
            return {"message": "something went wrong"}, 500

    def delete(self):
        return self.manager.db.drop_table(self.TABLE)

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
