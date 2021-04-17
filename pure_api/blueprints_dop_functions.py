from flask import jsonify, Blueprint, request
from sqalch_data.data.db_session import *
from sqalch_data.data.__all_models import *
from api_help_function import secure_check
from werkzeug.security import check_password_hash
import datetime

blueprint = Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users_questions/<user_email>', methods=['GET'])
@secure_check
def check_user_po_email(user_email):
    try:
        db_sess = create_session()
        user = db_sess.query(User).filter(User.email == user_email).first()
        assert user
        if check_password_hash(user.hashed_password, request.json['password']):
            return jsonify({'message': {'success': 'ok'}})
        else:
            return jsonify({'message': {'name': 'invalid password'}})
    except AssertionError:
        return jsonify({'message': {'name': 'user not found'}})


@blueprint.route('/api/users_from_email/<user_email>', methods=['GET'])
@secure_check
def id_from_email(user_email):
    try:
        db_sess = create_session()
        user = db_sess.query(User).filter(User.email == user_email).first()
        assert user
        return jsonify({'id': user.id})
    except AssertionError:
        return jsonify({'message': {'name': 'user not found'}})

