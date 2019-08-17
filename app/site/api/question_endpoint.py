import random

from app.decorators.api_decorators import json_serialize
from app.decorators.protected import protected
from app.site.api.ApiBase import ApiBase, validate_body
from app.site.exceptions import QuestionAlreadyExistsException
from app.site.models.dropdown import DropdownModel
from app.site.models.multi_choice import MultiChoiceModel
from app.site.models.fill_in import FillInModel

from flask import request


QUESTION_TYPES = ["dropdown", "multichoice", "fillin"]
MODELS = {
    "dropdown": DropdownModel,
    "multichoice": MultiChoiceModel,
    "fillin": FillInModel,
}


class QuestionSet(ApiBase):
    """
    /questions
    
    Returns nothing initially, requires queries to specify amount of questions
    ?dropdown=amount
    ?multi_choice=amount
    ?fill_in=amount
    """

    @json_serialize
    def get(self):
        self.manager.log.info(
            f"A set of random questions were requested."
        )

        args = dict(request.args)
        
        questions = []
        table_args = {}
        additional_args = {}
        

        for key, value in args.items():
            if key in QUESTION_TYPES:
                table_args[key] = value
                continue

            if key == "tags":
                value = value.split(",")
            elif value.isnumeric():
                value = int(value)

            additional_args[key] = value

        for table, amount in table_args.items():
            amount = int(amount)
            count = self.database.count("questions", type=table)
            if amount > count:
                message = f"{table} amount too high, max is: {count}"
                return {"message": message}, 400

            # Todo apply filter args
            tmp = list(self.database.find("questions", type=table, **additional_args))

            # Shuffle and extend so we can random results
            random.shuffle(tmp)
            questions.extend(tmp[:amount])

        random.shuffle(questions)
        return questions, 200

    @json_serialize
    @protected
    def post(self):
        body = request.get_json()

        if not isinstance(body, list):
            if not body.get("type"):
                return {
                    "message": "type is a required field when using this endpoint"
                    }, 400

            if body.get("type") not in QUESTION_TYPES:
                return {"message": "Unrecognized question type"}, 400

            model = MODELS[body["type"]]
            try:
                return self.database.insert_one(model.TABLE, body)
            except QuestionAlreadyExistsException as e:
                return {"message": str(e)}, 400


class QuestionSetById(ApiBase):
    @protected
    @json_serialize
    def delete(self, id_):
        delete_result = self.database.delete("questions", _id=id_)

        if delete_result.deleted_count:
            return {"message": "ok"}
        return {"message": "nothing deleted"}, 400


endpoints = {
    "/api/v1/questions": QuestionSet,
    "/api/v1/questions/<id_>": QuestionSetById,
}

__slots__ = [endpoints]