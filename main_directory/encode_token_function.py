from requests import get
from flask import jsonify, Blueprint, request
import json

blueprint = Blueprint(
    'encode_token_function',
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


@blueprint.route('/main_helper/get_new_token', methods=['POST'])
def get_token_new():
    if not request.json:
        return jsonify({'message': {'name': 'empty request'}}), 400
    if ('new_token' not in request.json and 'token' not in request.json
            and request.json['token'] != 'pass_main_token'):
        return jsonify({'message': {'name': 'invalid parameters'}}), 400

    write_pass_in_json(request.json['new_token'])
    return jsonify({'success': 'ok'}), 200


def make_request(data):
    resp = get('http://127.0.0.1:4010/get_password', json={'password_check': get_pass_from_json()})
    if resp:
        return {**data,
                'token': resp.json()[
                    'token']}
    # else:
    #     print(resp.json())


def money_in_rubles(string):
    value_ta = string.split()
    # print(value_ta)
    if value_ta[2][1:-1] == 'RUB':
        # print(float(value_ta[0]))
        return float(value_ta[0])
    response = get('https://www.cbr-xml-daily.ru/daily_json.js')
    if response:
        resp_js = response.json()
        # print(resp_js["Valute"][value_ta[2][1:-1]]['Value'] * float(value_ta[0]))
        try:
            return resp_js["Valute"][value_ta[2][1:-1]]['Value'] * float(value_ta[0])
        except Exception as e:
            return str(e)
