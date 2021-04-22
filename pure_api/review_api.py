from flask import request
from flask_restful import Resource
from sqalch_data.data.__all_models import *
from api_help_function import *
from all_parsers import parser_review, parser_put


class ReviewResource(Resource):
    @secure_check
    def get(self, review_id):
        try:
            db_sess = create_session()
            review = db_sess.query(Review).get(review_id)
            if not review:
                raise NotFoundError('review')
            return {'content': review.content,
                    'auction_id': review.auction_id,
                    'creator_id': review.creator_id}, 200
        except NotFoundError as error:
            return {'message': {'name': f'{str(error)} not found'}}, 404

    @secure_check
    def put(self, review_id):
        try:
            data = parser_put.parse_args().data
            db_sess = create_session()
            review = db_sess.query(Review).get(review_id)
            if not review:
                raise NotFoundError('review')
            for key in data:
                if key == 'content':
                    review.content = data[key]
                if key == 'auction_id':
                    auction = db_sess.query(Auction).get(data[key])
                    if not auction:
                        raise NotFoundError('auction')
                    review.auction = auction
                elif key == 'creator_id':
                    creator = db_sess.query(User).get(data[key])
                    if not creator:
                        raise NotFoundError('creator')
                    review.creator = creator
                else:
                    return {'message': {'name': 'review have no this property'}}, 405
            db_sess.commit()
            return {'message': {'success': 'ok'}}, 200
        except NotFoundError as error:
            return {'message': {'name': f'{str(error)} not found'}}, 404

    @secure_check
    def delete(self, review_id):
        try:
            db_sess = create_session()
            review = db_sess.query(Review).get(review_id)
            if not review:
                raise NotFoundError('review')
            db_sess.delete(review)
            db_sess.commit()
            return {'message': {'success': 'ok'}}, 200
        except NotFoundError as error:
            return {'message': {'name': f'{str(error)} not found'}}, 404


class ReviewListResource(Resource):
    @secure_check
    def get(self):
        # получает {'ids': [1, 2, 3, 4, 5, 6...]}
        if not request.json:
            return {'message': {'name': 'empty request'}}, 400
        if 'ids' not in request.json:
            return {'message': {'name': 'invalid parameters'}}, 400
        ids = request.json['ids']
        db_sess = create_session()
        payload = {'reviews': []}
        try:
            for review_id in ids:
                review = db_sess.query(Review).get(review_id)
                if not review:
                    raise NotFoundError(str(review_id))
                payload['reviews'].append(review.to_dict(only=('content',)))
            return payload, 200
        except NotFoundError as error:
            return {'message': {'name': f'{str(error)} review not found'}}, 404

    @secure_check
    def post(self):
        try:
            args = parser_review.parse_args()
            db_sess = create_session()
            review = Review()
            review.content = args.content

            auction = db_sess.query(Auction).get(args.auction_id)
            if not auction:
                raise NotFoundError('auction')
            review.auction = auction

            creator = db_sess.query(User).get(args.creator_id)
            if not creator:
                raise NotFoundError('creator')
            review.creator = creator

            db_sess.add(review)
            db_sess.commit()
            return {'message': {'success': 'ok'}}, 200
        except NotFoundError as error:
            return {'message': {'name': f'{str(error)} not found'}}, 404
