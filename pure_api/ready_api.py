from flask_restful import Resource
from sqalch_data.data.__all_models import *
from flask_jwt_extended import jwt_required


class ReadyResource(Resource):
    @jwt_required()
    def get(self):
        pass

    @jwt_required()
    def post(self):
        pass

    @jwt_required()
    def put(self):
        pass

    @jwt_required()
    def delete(self):
        pass


class ReadyListResource(Resource):
    @jwt_required()
    def get(self):
        pass

    @jwt_required()
    def post(self):
        pass

    @jwt_required()
    def put(self):
        pass

    @jwt_required()
    def delete(self):
        pass
