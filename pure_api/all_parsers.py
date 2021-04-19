from flask_restful.reqparse import RequestParser

parser_secure = RequestParser()
parser_secure.add_argument('token', required=True, type=str)


parser_put = RequestParser()
parser_put.add_argument('data', required=True, type=dict)

# парсер аргументов для пользователя
parser_user = RequestParser()
parser_user.add_argument('name', required=True, type=str)
parser_user.add_argument('surname', required=True, type=str)
parser_user.add_argument('patronymic', default='not_indicated', type=str)
parser_user.add_argument('age', required=True, type=int)
parser_user.add_argument('email', required=True, type=str)
parser_user.add_argument('position', default='not_indicated', type=str)
parser_user.add_argument('password', required=True, type=str)

# парсер для предмета
parser_thing = RequestParser()
parser_thing.add_argument('name', required=True, type=str)
parser_thing.add_argument('weight', default='not stated', type=str)
parser_thing.add_argument('height', default='not stated', type=str)
parser_thing.add_argument('long', default='not stated', type=str)
parser_thing.add_argument('width', default='not stated', type=str)
parser_thing.add_argument('about', default='not_indicated', type=str)
parser_thing.add_argument('colour', default='not_indicated', type=str)
parser_thing.add_argument('price', required=True, type=str)
parser_thing.add_argument('count', default=1, type=int)
parser_thing.add_argument('user_id', required=True, type=int)

# парсер аргументов для
parser_auction = RequestParser()

# парсер для отзыва
parser_review = RequestParser()

# парсер для фото
parser_photo = RequestParser()
parser_photo.add_argument('link', required=True, type=str)
parser_photo.add_argument('thing_id', required=False, type=int)
parser_photo.add_argument('user_id', required=False, type=int)
