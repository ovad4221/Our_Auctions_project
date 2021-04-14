from flask import Flask, make_response, url_for, jsonify, request, render_template, redirect, abort
from flask_restful import reqparse, abort, Api, Resource
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from sqalch_data.data.db_session import *
from sqalch_data.data.__all_models import *
import json
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
import datetime
from flask_jwt_extended import JWTManager

app = Flask(__name__)
api = Api(app)
app.config[
    'JWT_SECRET_KEY'] = 'Its_a_secret_key)#Это_очень!!длинная?и+секретнаяЁЁстрокаэ/|для2343подписи^^^токена#!'
app.config['JWT_EXPIRES'] = datetime.timedelta(hours=24)
app.config['JWT_IDENTITY_CLAIM'] = 'user'
app.config['JWT_HEADER_NAME'] = 'authorization'
app.jwt = JWTManager(app)

app.config['SECRET_KEY'] = '#Auction%Topic%Secret$%Key!!!'

params = {
    'title': 'Auctions',
    'style': '/static/css/style.css'
}

# login_manager = LoginManager()
# login_manager.init_app(app)


@app.route('/')
@app.route('/index')
def start():
    db_sess = create_session()
    return render_template('main_page.html', **params)


@app.route('/auction')
def auction_page():
    return  render_template('auction_page.html', **params)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
