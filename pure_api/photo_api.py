from flask_restful import Resource
from sqalch_data.data.__all_models import *
from flask_jwt_extended import jwt_required


class PhotoResource(Resource):
    @jwt_required()
    def get(self, photo_id):
        db_sess = create_session()
        return

    @jwt_required()
    def post(self):
        pass

    @jwt_required()
    def put(self, user_id):
        pass

    @jwt_required()
    def delete(self, user_id):
        pass


class PhotoListResource(Resource):
    pass

