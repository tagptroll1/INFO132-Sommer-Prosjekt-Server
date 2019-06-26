from app.site.api.ApiBase import ApiBase

from flask import request


class MultiChoice(ApiBase):
    def get(self):
        self.manager.log.info("All multichoice questions were requested.")
        return self.manager.db.find("multi_choice")

    def post(self):
        body = request.get_json()
        exists = False

        if len(self.manager.db.count("multi_choice")) > 0:
            exists = self.manager.find(**body)

        if not exists:
            self.manager.db.insert("multi_choice", body)

        self.manager.log.info("Multichoice question was posted.")
        return 201

    def delete(self):
        return self.manager.db.drop_table("multi_choice")
