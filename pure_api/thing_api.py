from flask import jsonify, request
from flask_restful import Resource
from sqalch_data.data.__all_models import *
from api_help_function import secure_check, check_si
from all_parsers import parser_thing, parser_put, parser_for_thi_lot


class ThingResource(Resource):
    @secure_check
    def get(self, thing_id):
        try:
            db_sess = create_session()
            thing = db_sess.query(Thing).get(thing_id)
            assert thing
            payload = dict()
            payload['photos'] = [photo.id for photo in thing.photos]
            payload['lots'] = [elem.lot_id for elem in thing.thi_lo_bits]
            return jsonify(
                {'thing': dict(tuple(thing.to_dict(only=(
                    'name', 'weight', 'height', 'long', 'width', 'about', 'colour', 'price', 'count',
                    'bought', 'created_date', 'user_id')).items()) + tuple(
                    payload.items()))})
        except AssertionError:
            return jsonify({'message': {'name': 'thing not found'}})

    @secure_check
    def put(self, thing_id):
        # можно обращаться по lot_id, это добавит вещь в лот,
        # а соответственно к вещи лот (need to add json with count)
        try:
            data = parser_put.parse_args().data
            db_sess = create_session()
            thing = db_sess.query(Thing).get(thing_id)
            assert thing, 'thing'
            for key in data:
                if key in ['name', 'weight', 'height', 'long', 'width', 'about', 'colour', 'start_price',
                           'price', 'count', 'bought']:
                    exec(f'thing.{key}=data[key]')
                elif key == 'user_id':
                    user = db_sess.query(User).get(data['user_id'])
                    assert user, 'user'
                    thing.user = user
                elif key == 'auction_id':
                    auction = db_sess.query(Auction).get(data['auction_id'])
                    assert auction, 'auction'
                    thing.auction = auction

                elif key == 'lot_id':
                    lot = db_sess.query(Lot).get(data[key])
                    assert lot, 'lot'
                    count = parser_for_thi_lot.parse_args().count
                    l_t_c = LotThingConnect()
                    l_t_c.count_thing = count
                    l_t_c.thing = thing
                    l_t_c.lot = lot
                    db_sess.add(l_t_c)

                else:
                    if key in ['created_date', 'id']:
                        return jsonify({'message': {'name': 'some of these properties cannot be changed'}})
                    return jsonify({'message': {'name': 'thing have no this property'}})
            db_sess.commit()
            return jsonify({'message': {'success': 'ok'}})
        except AssertionError as e:
            return jsonify({'message': {'name': f'{str(e)} not found'}})

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
        payload = {'things': []}
        try:
            for thing_id in ids:
                thing = db_sess.query(Thing).get(thing_id)
                assert thing, str(thing_id)
                if thing.photos:
                    photo_id = thing.photos[0].id
                else:
                    photo_id = -1
                payload['things'].append(dict(tuple(thing.to_dict(
                    only=('id', 'name', 'about', 'price', 'count')).items()) + tuple(
                    {'photo': photo_id}.items())))
            return jsonify(payload)
        except AssertionError as e:
            return jsonify({'message': {'name': f'{str(e)} thing not found'}})

    @secure_check
    def post(self):
        try:
            args = parser_thing.parse_args()
            db_sess = create_session()
            thing = Thing()
            thing.name = args.name
            if args.weight != 'not stated':
                assert check_si(args.weight), 'invalid form of weight'
            thing.weight = args.weight
            if args.height != 'not stated':
                assert check_si(args.height), 'invalid form of height'
            thing.height = args.height
            if args.long != 'not stated':
                assert check_si(args.long), 'invalid form of long'
            thing.long = args.long
            if args.width != 'not stated':
                assert check_si(args.width), 'invalid form of width'
            thing.width = args.width
            thing.about = args.about
            thing.colour = args.colour
            assert check_si(args.price), 'invalid form of price'
            thing.price = args.price
            thing.count = args.count

            user = db_sess.query(User).get(args.user_id)
            assert user, 'user not found'
            thing.user = user

            db_sess.add(thing)
            db_sess.commit()
            return jsonify({'message': {'success': 'ok', 'thing_id': thing.id}})
        except AssertionError as e:
            return jsonify({'message': {'name': str(e)}})
