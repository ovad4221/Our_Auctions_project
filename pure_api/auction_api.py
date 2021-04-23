from flask import request
from flask_restful import Resource
from sqalch_data.data.__all_models import *
from api_help_function import *
from all_parsers import parser_thing, parser_put, parser_for_thi_lot


class AuctionResource(Resource):
    @secure_check
    def get(self, auction_id):
        return {'message': {'name': 'Not Implemented'}}, 501

    @secure_check
    def put(self, auction_id):
        return {'message': {'name': 'Not Implemented'}}, 501

    @secure_check
    def delete(self, auction_id):
        return {'message': {'name': 'Not Implemented'}}, 501


class AuctionListResource(Resource):
    @secure_check
    def get(self):
        return {'message': {'name': 'Not Implemented'}}, 501

    @secure_check
    def post(self):
        return {'message': {'name': 'Not Implemented'}}, 501
