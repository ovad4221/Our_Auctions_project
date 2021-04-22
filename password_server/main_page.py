from flask import Flask, jsonify
from flask_restful import Api
from random import randint
from flask_restful.reqparse import RequestParser
import schedule

app = Flask(__name__)
api = Api(app)

secret_key = ''.join([chr(randint(10, 10 ** 4)) for _ in range(600)])
change_pas = True

parser_token = RequestParser()
parser_token.add_argument('password_check', required=True, type=str)


# try:
#     token = parser_secure.parse_args().token
#     assert check_token(token)
#     return func(*args, **kwargs)
# except AssertionError:
#     return jsonify({'message': {'name': 'invalid token'}})


@app.route('/get_password')
def main_ret():
    try:
        global secret_key

        token = parser_token.parse_args().password_check
        assert token == 'cock'

        return jsonify({'token': secret_key}), 200
    except AssertionError:
        return jsonify({'message': {'name': 'invalid token'}}), 403


app.run(port=4010, host='127.0.0.1')
