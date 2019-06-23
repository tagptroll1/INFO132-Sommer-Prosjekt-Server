from app.site.api.ApiBase import ApiBase

from flask import request


class MultiChoice(ApiBase):
    def get(self):
        self.manager.log.info("All multichoice questions were requested.")
        return self.manager.db.get_all("multi_choice")

    def post(self):
        body = request.get_json()
        if len(self.manager.db.get_all("multi_choice")) > 0:
            exists = self.manager.db.filter(
                "multi_choice",
                lambda x: x["question_text"] == body["question_text"]
            )
        else:
            exists = False

        if not exists:
            self.manager.db.insert(
                "multi_choice", body, conflict="update"
            )

        self.manager.log.info("Multichoice question was posted.")
        return 201

    def delete(self):
        return self.manager.db.drop_table("multi_choice")
