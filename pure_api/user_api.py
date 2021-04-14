from flask_restful import Resource
from sqalch_data.data.__all_models import *
from flask_jwt_extended import jwt_required


class UserResource(Resource):
    @jwt_required()
    def get(self, user_id):
        db_sess = create_session()
        user = db_sess.query(User).filter()
        return

    @jwt_required()
    def post(self, user_id):
        pass

    @jwt_required()
    def put(self, user_id):
        pass

    @jwt_required()
    def delete(self, user_id):
        pass


class UserListResource(Resource):
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
