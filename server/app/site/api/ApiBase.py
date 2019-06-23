from flask_restful import Resource


class ApiBase(Resource):
    @classmethod
    def add(cls, manager, path):
        cls.manager = manager
        manager.api.add_resource(cls, path)
