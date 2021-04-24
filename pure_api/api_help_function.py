from all_parsers import parser_secure
from requests import get
from flask import jsonify, Blueprint, request
import json

blueprint = Blueprint(
    'api_help_function',
    __name__,
    template_folder='templates'
)


def write_pass_in_json(new_token) -> bool:
    try:
        with open('pass_token.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps({'pass_token': new_token}))
            return True
    except Exception:
        return False


def get_pass_from_json() -> str:
    read_pass = ''.join(open('pass_token.json', 'r', encoding='utf-8').readlines())
    read_pass = json.loads(read_pass)
    return read_pass['pass_token']


@blueprint.route('/api_helper/get_new_token', methods=['POST'])
def get_token_new():
    if not request.json:
        return jsonify({'message': {'name': 'empty request'}}), 400
    if ('new_token' not in request.json and 'token' not in request.json
            and request.json['token'] != 'pass_api_token'):
        return jsonify({'message': {'name': 'invalid parameters'}}), 400

    write_pass_in_json(request.json['new_token'])
    return jsonify({'success': 'ok'}), 200


def check_token(token) -> bool:
    return token == \
           get('http://127.0.0.1:4010/get_password', json={'password_check': get_pass_from_json()}).json()[
               'token']


def secure_check(func):
    def ready_func(*args, **kwargs):
        try:
            token = parser_secure.parse_args().token
            assert check_token(token)
            return func(*args, **kwargs)
        except AssertionError:
            return {'message': {'name': 'invalid token'}}, 403

    return ready_func


def check_si(string):
    str1 = ''.join(string.split()[0].split('.'))
    return str1.isdigit()


class NotFoundError(Exception):
    pass


class ToManyError(Exception):
    pass


class NotCorrectFormError(Exception):
    pass
