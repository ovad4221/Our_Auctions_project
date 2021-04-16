from secret_keys import SITE_SECRET_KEY
from werkzeug.security import check_password_hash
from all_parsers import parser_secure
from flask import jsonify


def check_token(token):
    req_token = 'pbkdf2:sha256:150000$' + token
    return check_password_hash(req_token, SITE_SECRET_KEY)


def secure_check(func):

    def ready_func(*args, **kwargs):
        try:
            token = parser_secure.parse_args().token
            assert check_token(token)
            return func(*args, **kwargs)
        except AssertionError:
            return jsonify({'message': {'name': 'invalid token'}})

    return ready_func

