from app.site.api.ApiBase import ApiBase


class Dropdown(ApiBase):
    def get(self):
        self.manager.log.info("All dropdown questions were requested")

    def post(self):
        self.manager.log.info("Dropdown question was posted")

    def delete(self):
        ...