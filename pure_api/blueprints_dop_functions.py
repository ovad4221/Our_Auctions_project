from flask import jsonify, Blueprint, request
from sqalch_data.data.db_session import *
from sqalch_data.data.__all_models import *
from api_help_function import *
from werkzeug.security import check_password_hash
import datetime

blueprint = Blueprint(
    'blueprints_dop_functions',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users_questions/<user_email>', methods=['GET'])
@secure_check
def check_user_po_email(user_email):
    try:
        db_sess = create_session()
        user = db_sess.query(User).filter(User.email == user_email).first()
        if not user:
            raise NotFoundError('user')
        if user.check_password(request.json['password']):
            return jsonify({'message': {'success': 'ok'}})
        else:
            return jsonify({'message': {'name': 'invalid password'}})
    except NotFoundError as error:
        return {'message': {'name': f'{str(error)} not found'}}, 404


@blueprint.route('/api/users_from_email/<user_email>', methods=['GET'])
def id_from_email(user_email):
    try:
        db_sess = create_session()
        user = db_sess.query(User).filter(User.email == user_email).first()
        if not user:
            raise NotFoundError('user')
        return jsonify({'id': user.id})
    except NotFoundError as error:
        return {'message': {'name': f'{str(error)} not found'}}, 404
