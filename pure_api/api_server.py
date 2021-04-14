from user_api import *
from thing_api import *
from auction_api import *
from category_api import *
from photo_api import *
from ready_api import *
from review_api import *

from flask import Flask
from flask_restful import Api


app = Flask(__name__)
api = Api(app)

global_init('../pure_api/sqalch_data/db/main_database.db')

api.add_resource(UserResource, '/api/users/<int:user_id>')
api.add_resource(UserListResource, '/api/users')

api.add_resource(ThingResource, '/api/things/<int:thing_id>')
api.add_resource(ThingListResource, '/api/things')

api.add_resource(AuctionResource, '/api/auctions/<int:auction_id>')
api.add_resource(AuctionListResource, '/api/auctions')

api.add_resource(PhotoResource, '/api/photos/<int:photo_id>')
api.add_resource(PhotoListResource, '/api/photos')

api.add_resource(CategoryResource, '/api/categories/<int:category_id>')
api.add_resource(CategoryListResource, '/api/categories')

api.add_resource(ReviewResource, '/api/reviews/<int:review_id>')
api.add_resource(ReviewListResource, '/api/reviews')

api.add_resource(ReadyResource, '/api/readies/<int:ready_id>')
api.add_resource(ReadyListResource, '/api/readies')


app.run(port=5000, host='127.0.0.1')
