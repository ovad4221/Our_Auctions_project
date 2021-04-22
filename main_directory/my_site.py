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
import os

app = Flask(__name__)
params = {
    'title': 'Auctions',
    'style': '/static/css/style.css'
}
dict_to_add_thing_to_lot = {}

app.config['SECRET_KEY'] = '#Auction%Topic%Secret$%Key!!!'
app.config['UPLOAD_FOLDER'] = '/static/images/thing_user_images'

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
                                'hashed_password': form.password.data})).json()

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
                'count': form.count.data,
                'user_id': current_user.id})).json()['message']
        if 'success' in add_thing_request:
            return redirect("/account")
        return render_template('add_thing.html',
                               form=form, **params1, message=add_thing_request['name'])
    return render_template('add_thing.html', form=form, **params1)


@app.route('/edit_thing/<int:id>', methods=['GET', 'POST'])
def edit_thing(id):
    params1 = params.copy()
    params1['title'] = 'Редактирование вещи'
    form = AddThing()
    if request.method == "GET":
        edit_thing = get(f'http://127.0.0.1:5000/api/things/{id}', json=make_request({})).json()['thing']
        form.name.data = edit_thing['name']

        form.height.data = edit_thing['height'].split()[0]
        form.width.data = edit_thing['width'].split()[0]
        form.long.data = edit_thing['long'].split()[0]

        form.units_size.data = edit_thing['height'].split()[1]

        form.weight.data = edit_thing['weight'].split()[0]

        form.units_mass.data = edit_thing['weight'].split()[1]

        form.about.data = edit_thing['about']
        form.colour.data = edit_thing['colour']

        form.price.data = edit_thing['price'].split()[0]

        form.units_money.data = edit_thing['price'].split()[1]

        form.count.data = edit_thing['count']

    if form.validate_on_submit():
        edit_thing_request = put(f'http://127.0.0.1:5000/api/things/{id}',
                                 json=make_request({'data': {
                                     'name': form.name.data,
                                     'weight': str(form.weight.data) + ' ' + form.units_mass.data,
                                     'long': str(form.long.data) + ' ' + form.units_size.data,
                                     'width': str(form.width.data) + ' ' + form.units_size.data,
                                     'height': str(form.height.data) + ' ' + form.units_size.data,
                                     'about': form.about.data,
                                     'colour': form.colour.data,
                                     'price': str(form.price.data) + ' ' + form.units_money.data,
                                     'count': form.count.data,
                                     'user_id': current_user.id}})).json()['message']
        if 'success' in edit_thing_request:
            return redirect("/account")
        return render_template('add_thing.html',
                               form=form, **params1, message=edit_thing_request['name'])

    return render_template('add_thing.html', form=form, **params1)


@app.route('/delete_thing/<int:id>', methods=['GET', 'POST'])
def delete_thing(id):
    delete(f'http://127.0.0.1:5000/api/things/{id}', json=make_request({}))
    return redirect('/account')


@app.route('/delete_lot/<int:id>', methods=['GET', 'POST'])
def delete_lot(id):
    delete(f'http://127.0.0.1:5000/api/lots/{id}', json=make_request({}))
    return redirect('/account')


@app.route('/add_lot', methods=['GET', 'POST'])
def add_lot():
    params1 = params.copy()
    params1['title'] = 'Добавление вещи'
    form = LotForm()
    user_things_id = get(f'http://127.0.0.1:5000/api/users/{current_user.id}',
                         json=make_request({})).json()['user']['things']
    things = get('http://127.0.0.1:5000/api/things',
                 json=make_request({'ids': user_things_id})).json()['things']
    added_things = []

    for item in dict_to_add_thing_to_lot:
        added_thing_query = get(f'http://127.0.0.1:5000/api/things/{item}',
                                json=make_request({})).json()['thing']
        added_things.append({'id': item,
                             'name': added_thing_query['name'],
                             'count': dict_to_add_thing_to_lot[item]})

    if form.validate_on_submit():
        add_lot_query = post(f'http://127.0.0.1:5000/api/lots',
                         json=make_request({'list_ids': [(i, dict_to_add_thing_to_lot[i])
                                                         for i in dict_to_add_thing_to_lot],
                                            'user_id': current_user.id,
                                            'name': form.name.data,
                                            'about': form.about.data,
                                            'start_price': str(form.price.data) + ' ' + form.units_money.data})).json()
        if 'success' in add_lot_query['message']:
            dict_to_add_thing_to_lot.clear()
            return redirect('/account')
        return render_template('add_lot.html', form=form, **params1,
                               things=things, added_things=added_things,
                               message=add_lot_query['message'])

    return render_template('add_lot.html', form=form, **params1, things=things, added_things=added_things)


@app.route('/add_thing_to_lot/<int:id>', methods=['GET', 'POST'])
def add_thing_to_lot(id):
    global dict_to_add_thing_to_lot
    params1 = params.copy()
    params1['title'] = 'Добавление вещи в лот'
    form = AddThingToLot()
    if form.validate_on_submit():
        dict_to_add_thing_to_lot[id] = form.count.data
        return redirect('/add_lot')
    return render_template('add_thing_to_lot.html', form=form, **params1)


@app.route('/edit_lot/<int:lot_id>', methods=['GET', 'POST'])
def edit_lot(lot_id):
    global dict_to_add_thing_to_lot
    params1 = params.copy()
    params1['title'] = 'Редактирование лота'
    form = LotForm()

    user_things_id = get(f'http://127.0.0.1:5000/api/users/{current_user.id}',
                         json=make_request({})).json()['user']['things']
    things = get('http://127.0.0.1:5000/api/things',
                 json=make_request({'ids': user_things_id})).json()['things']

    lot = get(f'http://127.0.0.1:5000/api/lots/{lot_id}', json=make_request({})).json()['lot']

    for thing_i in lot['things']:
        dict_to_add_thing_to_lot[thing_i[0]] = thing_i[1]

    added_things = []

    for item in dict_to_add_thing_to_lot:
        added_thing_query = get(f'http://127.0.0.1:5000/api/things/{item}',
                                json=make_request({})).json()['thing']
        added_things.append({'id': item,
                             'name': added_thing_query['name'],
                             'count': dict_to_add_thing_to_lot[item]})

    if request.method == 'GET':

        form.name.data = lot['name']
        form.about.data = lot['about']

        form.price.data = lot['price'].split()[0]

        form.units_money.data = lot['price'].split()[1]

    if form.validate_on_submit():
        edit_lot_query = put(f'http://127.0.0.1:5000/api/lots{lot_id}',
                             json=make_request({'list_ids': [(i, dict_to_add_thing_to_lot[i])
                                                             for i in dict_to_add_thing_to_lot],
                                                'user_id': current_user.id,
                                                'name': form.name.data,
                                                'about': form.about.data,
                                                'start_price': str(
                                                    form.price.data) + ' ' + form.units_money.data})).json()
        if 'success' in edit_lot_query['message']:
            dict_to_add_thing_to_lot.clear()
            return redirect('/account')
        return render_template('add_lot.html', form=form, **params1,
                               things=things, added_things=added_things,
                               message=edit_lot_query['message'])

    return render_template('add_lot.html', form=form, **params1, things=things, added_things=added_things)


@app.route('/account', methods=['GET', 'POST'])
def account():
    params1 = params.copy()
    params1['title'] = 'Аккаунт'
    user_query = get(f'http://127.0.0.1:5000/api/users/{current_user.id}',
               json=make_request({})).json()['user']
    things = get('http://127.0.0.1:5000/api/things', json=make_request({'ids': user_query['things']})).json()['things']

    lots = []

    for lot_id in user_query['lots']:
        lot = get(f'http://127.0.0.1:5000/api/lots/{lot_id}', json=make_request({})).json()['lot']
        things_lot = []
        for thing_i in lot['things']:
            count_thing = thing_i[1]
            thing = get(f'http://127.0.0.1:5000/api/things/{thing_i[0]}', json=make_request({})).json()['thing']
            things_lot.append({'name': thing['name'], 'about': thing['about'],
                               'price': thing['price'], 'count': count_thing})
        lots.append({'id': lot_id, 'name': lot['name'],
                     'about': lot['about'], 'price': lot['price'],
                     'things': things_lot})

    return render_template('account.html', **params1, things=things, lots=lots)


@app.route('/del_thing_while_creating_lot/<int:id>', methods=['GET', 'POST'])
def del_thing_while_creating_lot(id):
    global dict_to_add_thing_to_lot
    dict_to_add_thing_to_lot.pop(id)

    return redirect('/add_lot')


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
