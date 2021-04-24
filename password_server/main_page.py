from flask import Flask, jsonify
from flask_restful import Api
import json
from flask_restful.reqparse import RequestParser
import os

app = Flask(__name__)
api = Api(app)
parser_token = RequestParser()
parser_token.add_argument('password_check', required=True, type=str)


def get_pass_from_json(f_name) -> str:
    read_pass = ''.join(open(f_name, 'r', encoding='utf-8').readlines())
    read_pass = json.loads(read_pass)
    return read_pass['pass_token']


@app.route('/get_password')
def main_ret():
    try:
        token = parser_token.parse_args().password_check
        assert token == get_pass_from_json('pass_token.json')

        return jsonify({'token': get_pass_from_json('secret_key.json')}), 200
    except AssertionError:
        return jsonify({'message': {'name': 'invalid token'}}), 403


os.startfile(r'help_file.py')
app.run(port=4010, host='127.0.0.1')
