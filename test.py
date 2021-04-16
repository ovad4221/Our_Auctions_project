from requests import get, put, post, delete
from werkzeug.security import generate_password_hash
from main_directory.encode_token_function import make_request

print(post('http://127.0.0.1:5000/api/users',
           json=make_request({'email': 'yang_aristotel1@mail.ru',
                                'name': 'Aristotel',
                               'surname': 'Afinsky',
                               'age': 24,
                               'position': 'filosaf',
                               'hashed_password': generate_password_hash('qwerty123')})).json())

print(get('http://127.0.0.1:5000/api/users/2', json=make_request({})).json())

# print(put('http://127.0.0.1:5000/api/users/2',
#           json=make_request({'data': {'email': 'yang_aristotel3@mail.ru'}})).json())

# print(delete('http://127.0.0.1:5000/api/users/2', json=make_request({})).json())
