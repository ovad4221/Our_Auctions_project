from werkzeug.security import check_password_hash
from all_parsers import parser_secure
from flask import jsonify
from requests import get


def check_token(token):
    return token == get('http://127.0.0.1:4010/get_password', json={'password_check': 'cock'}).json()['token']


def secure_check(func):
    def ready_func(*args, **kwargs):
        try:
            token = parser_secure.parse_args().token
            assert check_token(token)
            return func(*args, **kwargs)
        except AssertionError:
            return jsonify({'message': {'name': 'invalid token'}})

    return ready_func


def check_si(string):
    str1 = ''.join(string.split()[0].split('.'))
    return str1.isdigit()
