from flask import Flask, make_response, url_for, jsonify, request, render_template, redirect, abort
from flask_restful import reqparse, abort, Api, Resource
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from pure_api.sqalch_data.data.db_session import *
from pure_api.sqalch_data.data.__all_models import *
import json
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
import datetime
from models import *
from requests import get, put, post, delete
from werkzeug.security import generate_password_hash
from main_directory.encode_token_function import make_request
from current_user_class import User

app = Flask(__name__)
params = {
    'title': 'Auctions',
    'style': '/static/css/style.css'
}

app.config['SECRET_KEY'] = '#Auction%Topic%Secret$%Key!!!'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
@app.route('/index')
def start():
    return render_template('main_page.html', **params)


@app.route('/auction')
def auction_page():
    return render_template('auction_page.html', **params)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    params1 = params.copy()
    params1['title'] = 'Регистрация'
    form = RegisterUser()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('rega.html',
                                   form=form,
                                   message="Пароли не совпадают", **params1)

        query = post('http://127.0.0.1:5000/api/users',
             json=make_request({'email': form.email.data,
                                'name': form.name.data,
                                'surname': form.surname.data,
                                'patronymic': form.patronymic.data,
                                'age': form.age.data,
                                'position': form.position.data,
                                'hashed_password': generate_password_hash(form.password.data)})).json()

        if not 'success' in query['message']:
            return render_template('rega.html',
                                   form=form,
                                   message=query['message']['name'], **params1)

        return redirect('/login')

    return render_template('rega.html', form=form, **params1)


@app.route('/login', methods=['GET', 'POST'])
def login():
    params1 = params.copy()
    params1['title'] = 'Авторизация'
    form = LoginForm()
    if form.validate_on_submit():

        is_password_true = get(f'http://127.0.0.1:5000//api/users_questions/{form.email.data}',
                               json=make_request({'password': form.password.data})).json()['message']
        if 'success' in is_password_true:
            user = User(form.email.data)
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message=is_password_true['name'],
                               form=form, **params1)

    return render_template('login.html', form=form, **params1)


@app.route('/add_thing', methods=['GET', 'POST'])
def add_thing():
    params1 = params.copy()
    params1['title'] = 'Добавление вещи'
    form = AddThing()
    if form.validate_on_submit():
        add_thing_request = post('http://127.0.0.1:5000/api/things',
            json=make_request({
                'name': form.name.data,
                'weight': str(form.weight.data) + ' ' + form.units_mass.data,
                'long': str(form.long.data) + ' ' + form.units_size.data,
                'width': str(form.width.data) + ' ' + form.units_size.data,
                'height': str(form.height.data) + ' ' + form.units_size.data,
                'about': form.about.data,
                'colour': form.colour.data,
                'price': str(form.price.data) + ' ' + form.units_money.data,
                'count': form.price.data,
                'user_id': current_user.id})).json()['message']
        if 'success' in add_thing_request:
            return redirect("/account")
        return render_template('add_thing.html',
                               form=form, **params1, message=add_thing_request['name'])
    return render_template('add_thing.html', form=form, **params1)


@app.route('/account', methods=['GET', 'POST'])
def account():
    params1 = params.copy()
    params1['title'] = 'Аккаунт'
    return render_template('account.html', **params1)


@login_manager.user_loader
def load_user(user_id):
    info = get(f'http://127.0.0.1:5000/api/users/{user_id}', json=make_request({})).json()['user']
    user = User(info['email'])
    return user


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
