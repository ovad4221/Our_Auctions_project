from flask import jsonify, request
from flask_restful import Resource
from sqalch_data.data.__all_models import *
from api_help_function import secure_check
from all_parsers import parser_review, parser_put


class ReviewResource(Resource):
    @secure_check
    def get(self, review_id):
        try:
            db_sess = create_session()
            review = db_sess.query(Review).get(review_id)
            assert review, 'review not found'
            return jsonify({
                'content': review.content,
                'auction_id': review.auction_id,
                'creator_id': review.creator_id
            }), 200
        except AssertionError as e:
            return jsonify({'message': {'name': str(e)}}), 404

    @secure_check
    def put(self, review_id):
        try:
            data = parser_put.parse_args().data
            db_sess = create_session()
            review = db_sess.query(Review).get(review_id)
            assert review, 'photo not found'
            for key in data:
                if key == 'content':
                    review.content = data[key]
                if key == 'auction_id':
                    auction = db_sess.query(Auction).get(data[key])
                    assert auction, 'auction not found'
                    review.auction = auction
                elif key == 'creator_id':
                    creator = db_sess.query(User).get(data[key])
                    assert creator, 'creator not found'
                    review.creator = creator
                else:
                    return jsonify({'message': {'name': 'review have no this property'}}), 405
            db_sess.commit()
            return jsonify({'message': {'success': 'ok'}}), 200
        except AssertionError as e:
            return jsonify({'message': {'name': str(e)}}), 404

    @secure_check
    def delete(self, review_id):
        try:
            db_sess = create_session()
            review = db_sess.query(Review).get(review_id)
            assert review
            db_sess.delete(review)
            db_sess.commit()
            return jsonify({'message': {'success': 'ok'}}), 200
        except AssertionError:
            return jsonify({'message': {'name': 'review not found'}}), 404


class ReviewListResource(Resource):
    @secure_check
    def get(self):
        # получает {'ids': [1, 2, 3, 4, 5, 6...]}
        if not request.json:
            return jsonify({'message': {'name': 'empty request'}}), 400
        if 'ids' not in request.json:
            return jsonify({'message': {'name': 'invalid parameters'}}), 400
        ids = request.json['ids']
        db_sess = create_session()
        payload = {'reviews': []}
        try:
            for review_id in ids:
                review = db_sess.query(Review).get(review_id)
                assert review, str(review_id)
                payload['photos'].append(review.to_dict(only=('content',)))
            return jsonify(payload), 200
        except AssertionError as e:
            return jsonify({'message': {'name': f'{str(e)} review  not found'}}), 404

    @secure_check
    def post(self):
        try:
            args = parser_review.parse_args()
            db_sess = create_session()
            review = Review()
            review.content = args.content

            auction = db_sess.query(Auction).get(args.auction_id)
            assert auction, 'auction not found'
            review.auction = auction

            creator = db_sess.query(User).get(args.creator_id)
            assert creator, 'creator not found'
            review.creator = creator

            db_sess.add(review)
            db_sess.commit()
            return jsonify({'message': {'success': 'ok'}}), 200
        except AssertionError as e:
            return jsonify({'message': {'name': str(e)}}), 404
