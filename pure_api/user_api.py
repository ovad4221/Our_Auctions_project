from flask import request
from flask_restful import Resource
from sqalch_data.data.__all_models import *
from api_help_function import secure_check
from all_parsers import parser_user, parser_put


class UserResource(Resource):
    @secure_check
    def get(self, user_id):
        try:
            db_sess = create_session()
            user = db_sess.query(User).get(user_id)
            assert user
            payload = dict()
            payload['reviews'] = [review.id for review in user.reviews]
            payload['auctions'] = [auction.id for auction in user.auctions]
            payload['photos'] = [photo.id for photo in user.photos]
            payload['things'] = [thing.id for thing in user.things]
            payload['lots'] = [lot.id for lot in user.lots]
            payload['requisites'] = [requisite.id for requisite in user.requisites]
            return {'user': dict(
                tuple(user.to_dict(only=('email', 'name', 'surname', 'patronymic', 'age', 'position',
                                         'created_date', 'is_prime')).items()) + tuple(
                    payload.items()))}, 200
        except AssertionError:
            return {'message': {'name': 'user not found'}}, 404

    @secure_check
    def put(self, user_id):
        try:
            data = parser_put.parse_args().data
            db_sess = create_session()
            user = db_sess.query(User).get(user_id)
            assert user
            for key in data:
                if key in ['email', 'name', 'surname', 'patronymic', 'age', 'position']:
                    exec(f'user.{key}=data[key]')
                else:
                    if key in ['created_date', 'id']:
                        return {'message': {'name': 'some of these properties cannot be changed'}}, 403
                    return {'message': {'name': 'user have no this property'}}, 405
            db_sess.commit()
            return {'message': {'success': 'ok'}}, 200
        except sqlalchemy.exc.IntegrityError:
            return {'message': {'name': 'user with this email already exists'}}, 422
        except AssertionError:
            return {'message': {'name': 'user not found'}}, 404

    @secure_check
    def delete(self, user_id):
        try:
            db_sess = create_session()
            user = db_sess.query(User).get(user_id)
            assert user
            db_sess.delete(user)
            db_sess.commit()
            return {'message': {'success': 'ok'}}, 200
        except AssertionError:
            return {'message': {'name': 'user not found'}}, 404


class UserListResource(Resource):
    @secure_check
    def get(self):
        # получает {'ids': [1, 2, 3, 4, 5, 6...]}
        if not request.json:
            return {'message': {'name': 'empty request'}}, 400
        if 'ids' not in request.json:
            return {'message': {'name': 'invalid parameters'}}, 400
        ids = request.json['ids']
        db_sess = create_session()
        payload = {'users': []}
        try:
            for user_id in ids:
                user = db_sess.query(User).get(user_id)
                assert user, str(user_id)
                if user.photos:
                    photo_id = user.photos[0].id
                else:
                    photo_id = -1
                payload['users'].append(dict(tuple(user.to_dict(
                    only=('email', 'name', 'surname', 'patronymic')).items()) + tuple(
                    {'photo': photo_id}.items())))
            return payload, 200
        except AssertionError as e:
            return {'message': {'name': f'{str(e)} user not found'}}, 404

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
            user.set_password(args.password)
            db_sess.add(user)
            db_sess.commit()
            return {'message': {'success': 'ok'}}, 200
        except sqlalchemy.exc.IntegrityError:
            return {'message': {'name': 'user with this email already exists'}}, 422
