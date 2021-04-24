from user_api import *
from thing_api import *
from auction_api import *
from category_api import *
from photo_api import *
from ready_api import *
from review_api import *
from lot_api import *
from requisite_api import *
import blueprints_dop_functions
import api_help_function
from api_help_function import secure_check

from flask import Flask, jsonify
from flask_restful import Api


app = Flask(__name__)
api = Api(app)

global_init('../pure_api/sqalch_data/db/main_database.db')

app.register_blueprint(blueprints_dop_functions.blueprint)
app.register_blueprint(api_help_function.blueprint)


@app.route('/api/get_all_lots')
@secure_check
def get_all_lots():
    db_sess = create_session()
    lots = db_sess.query(Lot)
    lots = [lot.id for lot in lots]
    return jsonify({'lots': lots})


api.add_resource(UserResource, '/api/users/<int:user_id>')
api.add_resource(UserListResource, '/api/users')

api.add_resource(ThingResource, '/api/things/<int:thing_id>')
api.add_resource(ThingListResource, '/api/things')

api.add_resource(LotResource, '/api/lots/<int:lot_id>')
api.add_resource(LotListResource, '/api/lots')

api.add_resource(AuctionResource, '/api/auctions/<int:auction_id>')
api.add_resource(AuctionListResource, '/api/auctions')

api.add_resource(PhotoResource, '/api/photos/<int:photo_id>')
api.add_resource(PhotoListResource, '/api/photos')

api.add_resource(CategoryResource, '/api/categories/<int:category_id>')
api.add_resource(CategoryListResource, '/api/categories')

api.add_resource(ReviewResource, '/api/reviews/<int:review_id>')
api.add_resource(ReviewListResource, '/api/reviews')

api.add_resource(RequisiteResource, '/api/requisites/<int:requisite_id>')
api.add_resource(RequisiteListResource, '/api/requisites')

api.add_resource(ReadyResource, '/api/readies/<int:ready_id>')
api.add_resource(ReadyListResource, '/api/readies')


app.run(port=5000, host='127.0.0.1')
