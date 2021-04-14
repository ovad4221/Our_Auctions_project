from flask_restful.reqparse import RequestParser

# парсер аргументов для пользователя
parser_user = RequestParser()
parser_user.add_argument('name', required=True, type=str)
parser_user.add_argument('surname', required=True, type=str)
parser_user.add_argument('patronymic', required=True, type=str)
parser_user.add_argument('age', required=True, type=int)
parser_user.add_argument('email', required=True, type=str)
parser_user.add_argument('position', default='not indicated', type=str)
parser_user.add_argument('hashed_password', required=True, type=str)

# парсер аргументов для
parser_auction = RequestParser()

#
parser_thing = RequestParser()
