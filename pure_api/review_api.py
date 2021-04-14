from flask_restful import Resource
from sqalch_data.data.__all_models import *
from flask_jwt_extended import jwt_required


class ReviewResource(Resource):
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


class ReviewListResource(Resource):
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
