from flask_restful import Resource
from sqalch_data.data.__all_models import *


class PhotoResource(Resource):
    def get(self, photo_id):
        db_sess = create_session()
        return

    def post(self):
        pass

    def put(self, user_id):
        pass

    def delete(self, user_id):
        pass


class PhotoListResource(Resource):
    pass

