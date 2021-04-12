from flask import jsonify, Blueprint, request
from flask_restful import reqparse, abort, Api, Resource
from sqalch_data.data.db_session import *
from sqalch_data.data.__all_models import *
from all_parsers import parser_auction
import datetime


class AuctionResource(Resource):
    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class AuctionListResource(Resource):
    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
