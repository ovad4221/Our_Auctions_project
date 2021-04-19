from flask import jsonify, request
from flask_restful import Resource
from sqalch_data.data.__all_models import *
from api_help_function import secure_check
from all_parsers import parser_thing, parser_put


class ReviewResource(Resource):
    @secure_check
    def get(self, thing_id):
        pass

    @secure_check
    def put(self, thing_id):
        pass

    @secure_check
    def delete(self, thing_id):
        pass


class ReviewListResource(Resource):
    @secure_check
    def get(self):
        pass

    @secure_check
    def post(self):
        pass
