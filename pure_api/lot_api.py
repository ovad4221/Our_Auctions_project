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
            payload['things'] = [thing.id for thing in lot.things]
            return jsonify({'lot': dict(
                tuple(lot.to_dict(only=(
                    'name', 'about', 'start_price', 'price', 'buyer_id', 'auction_id',
                    'user_id')).items()) + tuple(
                    payload.items()))})
        except AssertionError as e:
            return jsonify({'message': {'name': str(e)}})

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
                    return jsonify({'message': {'name': 'lot have no this property'}})
            db_sess.commit()
            return jsonify({'message': {'success': 'ok'}})
        except AssertionError as e:
            return jsonify({'message': {'name': str(e)}})

    @secure_check
    def delete(self, lot_id):
        try:
            db_sess = create_session()
            lot = db_sess.query(Lot).get(lot_id)
            assert lot
            db_sess.delete(lot)
            db_sess.commit()
            return jsonify({'message': {'success': 'ok'}})
        except AssertionError:
            return jsonify({'message': {'name': 'lot not found'}})


class LotListResource(Resource):
    @secure_check
    def get(self):
        # получает {'ids': [1, 2, 3, 4, 5, 6...]}
        if not request.json:
            return jsonify({'message': {'name': 'empty request'}})
        if 'ids' not in request.json:
            return jsonify({'message': {'name': 'invalid parameters'}})
        ids = request.json['ids']
        db_sess = create_session()
        payload = {'lot': []}
        try:
            for lot_id in ids:
                lot = db_sess.query(Lot).get(lot_id)
                assert lot, str(lot_id)
                payload['lot'].append(lot.to_dict(only=('name', 'about', 'price')))
            return jsonify(payload)
        except AssertionError as e:
            return jsonify({'message': {'name': f'{str(e)} photo not found'}})

    @secure_check
    def post(self):
        try:
            args = parser_lot.parse_args()
            db_sess = create_session()
            lot = Lot()
            lot.name = args.name
            if args.about:
                lot.about = args.about

            assert check_si(args.start_price), 'invalid form of price'
            lot.start_price = lot.price = args.start_price

            user = db_sess.query(User).get(args.user_id)
            assert user, 'user not found'
            lot.user = user

            db_sess.add(lot)
            db_sess.commit()
            return jsonify({'message': {'success': 'ok'}})
        except AssertionError as e:
            return jsonify({'message': {'name': str(e)}})
