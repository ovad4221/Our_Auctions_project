from flask import jsonify, request
from flask_restful import Resource
from sqalch_data.data.__all_models import *
from api_help_function import secure_check
from all_parsers import parser_thing, parser_thing_put


class ThingResource(Resource):
    @secure_check
    def get(self, thing_id):
        try:
            db_sess = create_session()
            thing = db_sess.query(Thing).get(thing_id)
            assert thing
            photos = [photo.id for photo in thing.photos]
            return jsonify(
                {'thing': dict(list(thing.to_dict(only=(
                    'name', 'weight', 'height', 'long', 'width', 'about', 'colour', 'start_price', 'count',
                    'bought', 'created_date', 'user_id', 'auction_id')).iteams()) + list(
                    {'photos': photos}.items()))})
        except AssertionError:
            return jsonify({'message': {'name': 'thing not found'}})

    @secure_check
    def put(self, thing_id):
        try:
            data = parser_thing_put.parse_args().data
            db_sess = create_session()
            thing = db_sess.query(Thing).get(thing_id)
            who_is_not_found = 'thing'
            assert thing
            for key in data:
                if key in ['name', 'weight', 'height', 'long', 'width', 'about', 'colour', 'start_price',
                           'price', 'count', 'bought', 'user_id', 'auction_id']:
                    if key == 'user_id':
                        user = db_sess.query(User).get(data['user_id'])
                        who_is_not_found = 'user'
                        assert user
                        thing.user = user
                    elif key == 'auction_id':
                        auction = db_sess.query(Auction).get(data['auction_id'])
                        who_is_not_found = 'auction'
                        assert auction
                        thing.auction = auction
                    else:
                        exec(f'thing.{key}=data[key]')
                else:
                    if key in ['created_date', 'id']:
                        return jsonify({'message': {'name': 'some of these properties cannot be changed'}})
                    return jsonify({'message': {'name': 'thing have no this property'}})
            db_sess.commit()
            return jsonify({'message': {'success': 'ok'}})
        except AssertionError:
            return jsonify({'message': {'name': f'{who_is_not_found} not found'}})

    @secure_check
    def delete(self, thing_id):
        try:
            db_sess = create_session()
            thing = db_sess.query(Thing).get(thing_id)
            assert thing
            db_sess.delete(thing)
            db_sess.commit()
            return jsonify({'message': {'success': 'ok'}})
        except AssertionError:
            return jsonify({'message': {'name': 'thing not found'}})


class ThingListResource(Resource):
    @secure_check
    def get(self):
        # получает {'ids': [1, 2, 3, 4, 5, 6...]}
        if not request.json:
            return jsonify({'message': {'name': 'empty request'}})
        if 'ids' not in request.json:
            return jsonify({'message': {'name': 'invalid parameters'}})
        ids = request.json['ids']
        db_sess = create_session()
        id_not_found = -1
        payload = {'things': []}
        try:
            for thing_id in ids:
                id_not_found = thing_id
                thing = db_sess.query(Thing).get(thing_id)
                assert thing
                if thing.photos:
                    photo_id = thing.photos[0].id
                else:
                    photo_id = -1
                payload['things'].append(dict(list(thing.to_dict(
                    only=('name', 'about', 'start_price', 'count')).items()) + list(
                    {'photo': photo_id}.items())))
            return jsonify(payload)
        except AssertionError:
            return jsonify({'message': {'name': f'{id_not_found} user not found'}})

    @secure_check
    def post(self):
        try:
            args = parser_thing.parse_args()
            db_sess = create_session()
            thing = Thing()
            thing.name = args.name
            thing.weight = args.weight
            thing.height = args.height
            thing.long = args.long
            thing.width = args.width
            thing.about = args.about
            thing.colour = args.colour
            thing.start_price = thing.price = args.start_price
            thing.count = args.count

            user = db_sess.query(User).get(args.user_id)
            assert user
            thing.user = user

            db_sess.add(thing)
            db_sess.commit()
            return jsonify({'message': {'success': 'ok'}})
        except AssertionError:
            return jsonify({'message': {'name': 'user not found'}})
