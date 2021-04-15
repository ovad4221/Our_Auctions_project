from flask import jsonify
import sqlalchemy
from flask_restful import Resource
from sqalch_data.data.__all_models import *
from decode_token_function import check_token
from all_parsers import parser_user, parser_user_put, parser_secure


class UserResource(Resource):
    def get(self, user_id):
        try:
            token = parser_secure.parse_args().token
            assert check_token(token)
            db_sess = create_session()
            user = db_sess.query(User).filter(User.id == user_id).first()
            payload = {
                'email': user.email,
                'name': user.name,
                'surname': user.surname,
                'patronymic': user.patronymic,
                'age': user.age,
                'position': user.position}
            return jsonify(payload)
        except AssertionError:
            return jsonify({'message': {'name': 'invalid token'}})

    def put(self, user_id):
        try:
            data = parser_user_put.parse_args()
            db_sess = create_session()
            user = db_sess.query(User).get(User.id == user_id)
            for key in data:
                if key in user:
                    if key not in ['created_date', 'id']:
                        exec(f'user.{key}=data[key]')
                    else:
                        return jsonify({'message': {'name': 'some of these properties cannot be changed'}})
                else:
                    return jsonify({'message': {'name': 'user have no this property'}})
            db_sess.commit()
            return jsonify({
                'success': 'ok'
            })
        except sqlalchemy.exc.IntegrityError:
            return jsonify({'message': {'name': 'user with this email already exists'}})

    def delete(self, user_id):
        pass


class UserListResource(Resource):
    def get(self):
        pass

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
            return jsonify({
                'success': 'ok'
            })
        except sqlalchemy.exc.IntegrityError:
            return jsonify({'message': {'name': 'user with this email already exists'}})

    def delete(self):
        pass
