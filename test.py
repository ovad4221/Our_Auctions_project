from requests import get, put, post, delete
from werkzeug.security import generate_password_hash
from main_directory.encode_token_function import make_request

# print(post('http://127.0.0.1:5000/api/users',
#            json=make_request({'email': 'yang_aristotel1@mail.ru',
#                               'name': 'Aristotel',
#                               'surname': 'Afinsky',
#                               'age': 24,
#                               'position': 'filosaf',
#                               'hashed_password': generate_password_hash('qwerty123')})).json())

# print(get('http://127.0.0.1:5000/api/users/2', json=make_request({})).json())

# print(put('http://127.0.0.1:5000/api/users/2',
#           json=make_request({'data': {'email': 'yang_aristotel3@mail.ru'}})).json())

# print(delete('http://127.0.0.1:5000/api/users/2', json=make_request({})).json())

# print(get('http://127.0.0.1:5000/api/users/yang_aristotel@mail.ru',
#           json=make_request({'password': 'qwerty123'})).json())

# print(post('http://127.0.0.1:5000/api/things',
#            json=make_request({
#                'name': 'Bluetooth душ',
#                'weight': 700,
#                'long': 20,
#                'width': 4,
#                'about': 'Вот так вот',
#                'colour': 'white',
#                'start_price': 10000,
#                'count': 1,
#                'user_id': 2})).json())

# print(put('http://127.0.0.1:5000/api/things/1',
#           json=make_request({'data': {'name': 'Огромный розовый член'}})).json())

# print(delete('http://127.0.0.1:5000/api/things/1', json=make_request({})).json())

# print(get('http://127.0.0.1:5000/api/things', json=make_request({'ids': [1, 2]})).json())
