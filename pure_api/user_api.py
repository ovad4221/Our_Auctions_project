from flask import jsonify
import sqlalchemy
from flask_restful import Resource
from sqalch_data.data.__all_models import *
from api_help_function import secure_check
from all_parsers import parser_user, parser_user_put


class UserResource(Resource):
    @secure_check
    def get(self, user_id):
        try:
            db_sess = create_session()
            user = db_sess.query(User).get(user_id)
            assert user
            return jsonify(
                {'user': user.to_dict(only=('email', 'name', 'surname', 'patronymic', 'age', 'position'))})
        except AssertionError:
            return jsonify({'message': {'name': 'user not found'}})

    @secure_check
    def put(self, user_id):
        try:
            data = parser_user_put.parse_args().data
            db_sess = create_session()
            user = db_sess.query(User).get(user_id)
            assert user
            for key in data:
                if key in ['email', 'name', 'surname', 'patronymic', 'age', 'position']:
                    exec(f'user.{key}=data[key]')
                else:
                    if key in ['created_date', 'id']:
                        return jsonify({'message': {'name': 'some of these properties cannot be changed'}})
                    return jsonify({'message': {'name': 'user have no this property'}})
            db_sess.commit()
            return jsonify({'message': {'success': 'ok'}})
        except sqlalchemy.exc.IntegrityError:
            return jsonify({'message': {'name': 'user with this email already exists'}})
        except AssertionError:
            return jsonify({'message': {'name': 'user not found'}})

    @secure_check
    def delete(self, user_id):
        try:
            db_sess = create_session()
            user = db_sess.query(User).get(user_id)
            assert user
            db_sess.delete(user)
            db_sess.commit()
            return jsonify({'message': {'success': 'ok'}})
        except AssertionError:
            return jsonify({'message': {'name': 'user not found'}})


class UserListResource(Resource):
    @secure_check
    def get(self):
        pass

    @secure_check
    def post(self):
        try:
            args = parser_user.parse_args()
            db_sess = create_session()
            user = User()
            user.name = args.name
            user.surname = args.surname
            user.patronymic = args.patronymic
            user.age = args.age
            user.email = args.email
            user.position = args.position
            user.hashed_password = args.hashed_password
            db_sess.add(user)
            db_sess.commit()
            return jsonify({'message': {'name': 'user not found'}})
        except sqlalchemy.exc.IntegrityError:
            return jsonify({'message': {'name': 'user with this email already exists'}})
