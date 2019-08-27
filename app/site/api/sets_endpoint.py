from app.decorators.api_decorators import json_serialize
from app.decorators.protected import protected
from app.site.api.ApiBase import ApiBase, validate_body

from flask import request


class QuestionSearchSet(ApiBase):
    @json_serialize
    @protected
    def put(self):
        body = request.get_json()

        ids = body.get("ids")
        new_tags = body.get("tag")

        if not isinstance(ids, list):
            ids = [ids]

        if not isinstance(new_tags, list):
            new_tags = [new_tags]

        if not ids:
            return {"message": "No ids given"}, 400

        if not new_tags:
            return {"message": "No tags given"}, 400

        questions = list(self.database.find("questions", _id=ids))
        
        results = []
        for question in questions:
            # Remove duplications
            tags = list({*question["tags"], *new_tags})
            tmp = self.database.edit(
                "questions",
                {"_id": question["_id"]},
                {"tags": tags}
            )
            results.append(tmp)

        return results


endpoints = {
    "/api/v1/searchset": QuestionSearchSet
}

__slots__ = [endpoints]
