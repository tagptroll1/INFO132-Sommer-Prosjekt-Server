import random

from app.decorators.api_decorators import json_serialize
from app.site.api.ApiBase import ApiBase

from flask import request

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

        for table, amount in args.items():
            amount = int(amount)
            count = self.database.count(table)
            if amount > count:
                message = f"{table} amount too high, max is: {amount}"
                return {"message": message}, 400

            # Todo apply filter args
            tmp = list(self.database.find(table))

            # Shuffle and extend so we can random results
            random.shuffle(tmp)
            questions.extend(tmp[:amount])

        random.shuffle(questions)
        return questions, 200




endpoints = {
    "/api/v1/questions": QuestionSet,
}

__slots__ = [endpoints]