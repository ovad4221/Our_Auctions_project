from flask import request
from flask_restful import Resource
from sqalch_data.data.__all_models import *
from api_help_function import *
from all_parsers import parser_photo, parser_put


class PhotoResource(Resource):
    @secure_check
    def get(self, photo_id):
        try:
            db_sess = create_session()
            photo = db_sess.query(Photo).get(photo_id)
            if not photo:
                raise NotFoundError('photo')
            return {'link': photo.link,
                    'thing_id': photo.thing_id,
                    'user_id': photo.user_id}, 200
        except NotFoundError as error:
            return {'message': {'name': f'{str(error)} not found'}}, 404

    @secure_check
    def put(self, photo_id):
        try:
            data = parser_put.parse_args().data
            db_sess = create_session()
            photo = db_sess.query(Photo).get(photo_id)
            if not photo:
                raise NotFoundError('photo')
            for key in data:
                if key == 'link':
                    photo.link = data[key]
                if key == 'thing_id':
                    thing = db_sess.query(Thing).get(data[key])
                    if not thing:
                        raise NotFoundError('thing')
                    photo.thing = thing
                elif key == 'user_id':
                    user = db_sess.query(User).get(data[key])
                    if not user:
                        raise NotFoundError('user')
                    photo.user = user
                else:
                    return {'message': {'name': 'photo have no this property'}}, 405
            db_sess.commit()
            return {'message': {'success': 'ok'}}, 200
        except NotFoundError as error:
            return {'message': {'name': f'{str(error)} not found'}}, 404

    @secure_check
    def delete(self, photo_id):
        try:
            db_sess = create_session()
            photo = db_sess.query(Photo).get(photo_id)
            if not photo:
                raise NotFoundError('photo')
            db_sess.delete(photo)
            db_sess.commit()
            return {'message': {'success': 'ok'}}, 200
        except NotFoundError as error:
            return {'message': {'name': f'{str(error)} not found'}}, 404


class PhotoListResource(Resource):
    @secure_check
    def get(self):
        # получает {'ids': [1, 2, 3, 4, 5, 6...]}
        if not request.json:
            return {'message': {'name': 'empty request'}}, 400
        if 'ids' not in request.json:
            return {'message': {'name': 'invalid parameters'}}, 400
        ids = request.json['ids']
        db_sess = create_session()
        payload = {'photos': []}
        try:
            for photo_id in ids:
                photo = db_sess.query(Photo).get(photo_id)
                if not photo:
                    raise NotFoundError(str(photo_id))
                payload['photos'].append(photo.to_dict(only=('link',)))
            return payload, 200
        except NotFoundError as error:
            return {'message': {'name': f'{str(error)} photo not found'}}, 404

    @secure_check
    def post(self):
        try:
            args = parser_photo.parse_args()
            db_sess = create_session()
            photo = Photo()
            photo.link = args.link

            thing = db_sess.query(Thing).get(args.thing_id)
            if not thing:
                raise NotFoundError('thing')
            photo.thing = thing

            user = db_sess.query(User).get(args.user_id)
            if not user:
                raise NotFoundError('user')
            photo.user = user

            db_sess.add(photo)
            db_sess.commit()
            return {'message': {'success': 'ok'}}, 200
        except NotFoundError as error:
            return {'message': {'name': f'{str(error)} not found'}}, 404
