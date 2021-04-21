from flask import jsonify, request
from flask_restful import Resource
from sqalch_data.data.__all_models import *
from api_help_function import secure_check, check_si
from all_parsers import parser_lot, parser_put


class LotResource(Resource):
    @secure_check
    def get(self, lot_id):
        try:
            db_sess = create_session()
            lot = db_sess.query(Lot).get(lot_id)
            assert lot, 'lot not found'
            payload = dict()
            payload['things'] = [elem.thing_id for elem in lot.lo_thi_bits]
            return jsonify({'lot': dict(
                tuple(lot.to_dict(only=(
                    'name', 'about', 'start_price', 'price', 'buyer_id', 'auction_id',
                    'user_id')).items()) + tuple(
                    payload.items()))}), 200
        except AssertionError as e:
            return jsonify({'message': {'name': str(e)}}), 404

    @secure_check
    def put(self, lot_id):
        try:
            data = parser_put.parse_args().data
            db_sess = create_session()
            lot = db_sess.query(Lot).get(lot_id)
            assert lot, 'lot not found'
            for key in data:
                if key in ['name', 'about', 'start_price', 'price', 'buyer_id']:
                    exec(f'lot.{key}=data[key]')
                elif key == 'auction_id':
                    auction = db_sess.query(Auction).get(data[key])
                    assert auction, 'auction not found'
                    lot.auction = auction
                elif key == 'user_id':
                    user = db_sess.query(User).get(data[key])
                    assert user, 'user not found'
                    lot.user = user
                else:
                    return jsonify({'message': {'name': 'lot have no this property'}}), 405
            db_sess.commit()
            return jsonify({'message': {'success': 'ok'}}), 200
        except AssertionError as e:
            return jsonify({'message': {'name': str(e)}}), 404

    @secure_check
    def delete(self, lot_id):
        try:
            db_sess = create_session()
            lot = db_sess.query(Lot).get(lot_id)
            assert lot
            for lo_thi_bit in lot.lo_thi_bits:
                db_sess.delete(lo_thi_bit)
            db_sess.delete(lot)
            db_sess.commit()
            return jsonify({'message': {'success': 'ok'}}), 200
        except AssertionError:
            return jsonify({'message': {'name': 'lot not found'}}), 404


class LotListResource(Resource):
    @secure_check
    def get(self):
        # получает {'ids': [1, 2, 3, 4, 5, 6...]}
        if not request.json:
            return jsonify({'message': {'name': 'empty request'}}), 400
        if 'ids' not in request.json:
            return jsonify({'message': {'name': 'invalid parameters'}}), 400
        ids = request.json['ids']
        db_sess = create_session()
        payload = {'lot': []}
        try:
            for lot_id in ids:
                lot = db_sess.query(Lot).get(lot_id)
                assert lot, str(lot_id)
                payload['lot'].append(lot.to_dict(only=('name', 'about', 'price')))
            return jsonify(payload), 200
        except AssertionError as e:
            return jsonify({'message': {'name': f'{str(e)} photo not found'}}), 404

    @secure_check
    def post(self):
        # на подачу так же идет json с списком (list_ids) пар (id, count)
        try:
            args = parser_lot.parse_args()
            db_sess = create_session()
            lot = Lot()
            lot.name = args.name
            if args.about:
                lot.about = args.about

            assert request.json, 'empty request'
            assert 'list_ids' in request.json, 'invalid parameters'
            for thing_id, count in request.json['list_ids']:
                thing = db_sess.query(Thing).get(thing_id)
                assert thing, f'{thing_id} thing not found'
                sum_ca = sum([thi_lo_bit.count for thi_lo_bit in thing.thi_lo_bits])
                assert sum_ca + count <= thing.count, f'{count + sum_ca - thing.count} objects'
                l_t_c = LotThingConnect()
                l_t_c.count_thing = count
                l_t_c.thing = thing
                l_t_c.lot = lot
                db_sess.add(l_t_c)

            assert check_si(args.start_price), 'invalid form of price'
            lot.start_price = lot.price = args.start_price

            user = db_sess.query(User).get(args.user_id)
            assert user, 'user not found'
            lot.user = user

            db_sess.add(lot)
            db_sess.commit()
            return jsonify({'message': {'success': 'ok'}}), 200
        except AssertionError as e:
            return jsonify({'message': {'name': str(e)}}), 404
