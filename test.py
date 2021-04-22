from requests import get, put, post, delete
from werkzeug.security import generate_password_hash
from main_directory.encode_token_function import make_request

# print(post('http://127.0.0.1:5000/api/users',
#            json=make_request({'email': 'yang_aristotel1@mail.ru',
#                               'name': 'Aristotel',
#                               'surname': 'Afinsky',
#                               'age': 24,
#                               'position': 'filosaf',
#                               'password': 'qwerty123'})))

# print(get('http://127.0.0.1:5000/api/users/1', json=make_request({})))

# print(put('http://127.0.0.1:5000/api/users/1',
#           json=make_request({'data': {'email': 'yang_aristotel3@mail.ru'}})).json())

# print(delete('http://127.0.0.1:5000/api/users/2', json=make_request({})).json())

# print(get('http://127.0.0.1:5000/api/users_questions/yang_aristotel@mail.ru',
#           json=make_request({'password': 'qwerty123'})).json())

# print(post('http://127.0.0.1:5000/api/things',
#            json=make_request({
#                'name': 'Bluetooth душ',
#                'weight': '300 гр',
#                'long': '20 см',
#                'width': '4 см',
#                'about': 'Вот так вот',
#                'colour': 'white',
#                'price': '10000 ₽',
#                'count': 1,
#                'user_id': 1})).json())

# print(put('http://127.0.0.1:5000/api/things/1',
#           json=make_request({'data': {'name': 'Огромный розовый член'}})).json())

# print(delete('http://127.0.0.1:5000/api/things/1', json=make_request({})).json())

# print(get('http://127.0.0.1:5000/api/things', json=make_request({'ids': [1, 2]})).json())
# print(get('http://127.0.0.1:5000/api/things/1', json=make_request({})).json())

# print(get('http://127.0.0.1:4010/get_password', json={'password_check': 'cock'}))

# print(post('http://127.0.0.1:5000/api/lots',
#            json=make_request({
#                'name': 'лот 1',
#                'about': 'Вот так вот',
#                'start_price': '123 ЫЫы',
#                'user_id': 1,
#                'list_ids': [(1, 7), (2, 4), (3, 5)]})).json())
