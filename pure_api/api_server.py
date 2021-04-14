from sqalch_data.data.db_session import *
from sqalch_data.data.__all_models import *
from user_api import *
from thing_api import *
from auction_api import *
from flask import Flask, make_response, url_for, jsonify, request, render_template, redirect, abort
from flask_restful import reqparse, abort, Api, Resource


app = Flask(__name__)
api = Api(app)

global_init('../sqalch_data/db/main_database.db')
api.add_resource(UserResource, '/api/user/news')

# для одного объекта
api.add_resource(news_resources.NewsResource, '/api/v2/news/<int:news_id>')

app.run(port=5000, host='127.0.0.1')
