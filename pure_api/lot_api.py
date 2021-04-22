from flask import request
from flask_restful import Resource
from sqalch_data.data.__all_models import *
from api_help_function import *
from all_parsers import parser_lot, parser_put


class LotResource(Resource):
    @secure_check
    def get(self, lot_id):
        try:
            db_sess = create_session()
            lot = db_sess.query(Lot).get(lot_id)
            if not lot:
                raise NotFoundError('lot')
            payload = dict()
            payload['things'] = [(elem.thing_id, elem.count_thing) for elem in lot.lo_thi_bits]
            return {'lot': dict(tuple(lot.to_dict(only=(
                'name', 'about', 'start_price', 'price', 'buyer_id', 'auction_id',
                'user_id')).items()) + tuple(
                payload.items()))}, 200
        except NotFoundError as error:
            return {'message': {'name': f'{str(error)} not found'}}, 404

    @secure_check
    def put(self, lot_id):
        try:
            data = parser_put.parse_args().data
            db_sess = create_session()
            lot = db_sess.query(Lot).get(lot_id)
            if not lot:
                raise NotFoundError('lot')
            for key in data:
                if key in ['name', 'about', 'start_price', 'price', 'buyer_id']:
                    exec(f'lot.{key}=data[key]')
                elif key == 'auction_id':
                    auction = db_sess.query(Auction).get(data[key])
                    if not auction:
                        raise NotFoundError('auction')
                    lot.auction = auction
                elif key == 'user_id':
                    user = db_sess.query(User).get(data[key])
                    if not user:
                        raise NotFoundError('user')
                    lot.user = user
                else:
                    return {'message': {'name': 'lot have no this property'}}, 405
            db_sess.commit()
            return {'message': {'success': 'ok'}}, 200
        except NotFoundError as error:
            return {'message': {'name': f'{str(error)} not found'}}, 404

    @secure_check
    def delete(self, lot_id):
        try:
            db_sess = create_session()
            lot = db_sess.query(Lot).get(lot_id)
            if not lot:
                raise NotFoundError('lot')
            for lo_thi_bit in lot.lo_thi_bits:
                db_sess.delete(lo_thi_bit)
            db_sess.delete(lot)
            db_sess.commit()
            return {'message': {'success': 'ok'}}, 200
        except NotFoundError as error:
            return {'message': {'name': f'{str(error)} not found'}}, 404


class LotListResource(Resource):
    @secure_check
    def get(self):
        # получает {'ids': [1, 2, 3, 4, 5, 6...]}
        if not request.json:
            return {'message': {'name': 'empty request'}}, 400
        if 'ids' not in request.json:
            return {'message': {'name': 'invalid parameters'}}, 400
        ids = request.json['ids']
        db_sess = create_session()
        payload = {'lots': []}
        try:
            for lot_id in ids:
                lot = db_sess.query(Lot).get(lot_id)
                if not lot:
                    raise NotFoundError(str(lot_id))
                payload['lots'].append(dict(
                    tuple(lot.to_dict(only=('name', 'about', 'price')).items()) + tuple(
                        {'things': [(elem.thing_id, elem.count_thing) for elem in lot.lo_thi_bits]}.items())))
            return payload, 200
        except NotFoundError as error:
            return {'message': {'name': f'{str(error)} lot not found'}}, 404

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

            if not check_si(args.start_price):
                raise NotCorrectFormError('start_price')
            lot.start_price = lot.price = args.start_price

            user = db_sess.query(User).get(args.user_id)
            if not user:
                raise NotFoundError('user')
            lot.user = user

            if not request.json:
                return {'message': {'name': 'empty request'}}, 400
            if 'ids' not in request.json:
                return {'message': {'name': 'invalid parameters'}}, 400

            for thing_id, count in request.json['list_ids']:
                thing = db_sess.query(Thing).get(thing_id)
                if not thing:
                    raise NotFoundError(f'{thing_id} thing')
                sum_ca = sum([thi_lo_bit.count_thing for thi_lo_bit in thing.thi_lo_bits])
                if not sum_ca + int(count) <= thing.count:
                    raise ToManyError(f'not enough objects ({count + sum_ca - thing.count})')
                l_t_c = LotThingConnect()
                l_t_c.count_thing = count
                l_t_c.thing = thing
                l_t_c.lot = lot
                db_sess.add(l_t_c)

            db_sess.add(lot)
            db_sess.commit()
            return {'message': {'success': 'ok'}}, 200
        except NotCorrectFormError as error:
            return {'message': {'name': f'invalid form of {str(error)}'}}, 412
        except NotFoundError as error:
            return {'message': {'name': f'{str(error)} not found'}}, 404
        except ToManyError as error:
            return {'message': {'name': str(error)}}, 412
