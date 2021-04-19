from flask import jsonify, request
from flask_restful import Resource
from sqalch_data.data.__all_models import *
from api_help_function import secure_check
from all_parsers import parser_photo, parser_put


class PhotoResource(Resource):
    @secure_check
    def get(self, photo_id):
        try:
            db_sess = create_session()
            photo = db_sess.query(Photo).get(photo_id)
            assert photo, 'photo not found'
            return jsonify({
                'link': photo.link,
                'thing_id': photo.thing_id,
                'user_id': photo.user_id
            })
        except AssertionError as e:
            return jsonify({'message': {'name': str(e)}})

    @secure_check
    def put(self, photo_id):
        try:
            data = parser_put.parse_args().data
            db_sess = create_session()
            photo = db_sess.query(Photo).get(photo_id)
            assert photo, 'photo not found'
            for key in data:
                if key == 'link':
                    photo.link = data[key]
                if key == 'thing_id':
                    thing = db_sess.query(Thing).get(data[key])
                    assert thing, 'thing not found'
                    photo.thing = thing
                elif key == 'user_id':
                    user = db_sess.query(User).get(data[key])
                    assert user, 'user not found'
                    photo.user = user
                else:
                    return jsonify({'message': {'name': 'photo have no this property'}})
            db_sess.commit()
            return jsonify({'message': {'success': 'ok'}})
        except AssertionError as e:
            return jsonify({'message': {'name': str(e)}})

    @secure_check
    def delete(self, photo_id):
        try:
            db_sess = create_session()
            photo = db_sess.query(Photo).get(photo_id)
            assert photo
            db_sess.delete(photo)
            db_sess.commit()
            return jsonify({'message': {'success': 'ok'}})
        except AssertionError:
            return jsonify({'message': {'name': 'photo not found'}})


class PhotoListResource(Resource):
    @secure_check
    def post(self):
        try:
            args = parser_photo.parse_args()
            db_sess = create_session()
            photo = Photo()
            photo.link = args.link

            thing = db_sess.query(Thing).get(args.thing_id)
            assert thing, 'thing not found'
            photo.thing = thing

            user = db_sess.query(User).get(args.user_id)
            assert user, 'user not found'
            photo.user = user

            db_sess.add(photo)
            db_sess.commit()
            return jsonify({'message': {'success': 'ok'}})
        except AssertionError as e:
            return jsonify({'message': {'name': str(e)}})

