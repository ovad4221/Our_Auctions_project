from flask import request
from flask_restful import Resource
from sqalch_data.data.__all_models import *
from api_help_function import *
from all_parsers import parser_thing, parser_put, parser_for_thi_lot


class ReadyResource(Resource):
    @secure_check
    def get(self, ready_id):
        return {'message': {'name': 'Not Implemented'}}, 501

    @secure_check
    def put(self, ready_id):
        return {'message': {'name': 'Not Implemented'}}, 501

    @secure_check
    def delete(self, ready_id):
        return {'message': {'name': 'Not Implemented'}}, 501


class ReadyListResource(Resource):
    @secure_check
    def get(self):
        return {'message': {'name': 'Not Implemented'}}, 501

    @secure_check
    def post(self):
        return {'message': {'name': 'Not Implemented'}}, 501
