from flask_restful.reqparse import RequestParser

parser_user = RequestParser()
# parser_user.add_argument('user_id', required=True)
# parser_user.add_argument('name', required=True)
# parser_user.add_argument('surname', required=True)
# parser_user.add_argument('patronymic', required=True, type=bool)
# parser_user.add_argument('age', required=True, type=bool)
# parser_user.add_argument('email', required=True, type=int)
# parser_user.add_argument('position', required=True)
# parser_user.add_argument('patronymic', required=True, type=bool)
# parser_user.add_argument('age', required=True, type=bool)
# parser_user.add_argument('email', required=True, type=int)

parser_auction = RequestParser()

parser_thing = RequestParser()
