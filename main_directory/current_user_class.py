from flask_login import UserMixin
from requests import get
from main_directory.encode_token_function import make_request


class User(UserMixin):
    def __init__(self, email):
        self.id = get(f'http://127.0.0.1:5000/api/users_from_email/{email}').json()['id']
        self.email = email
        self.info = get(f'http://127.0.0.1:5000/api/users/{self.id}', json=make_request({})).json()['user']
        self.name = self.info['name']
        self.surname = self.info['surname']
        self.patronymic = self.info['patronymic']
        self.age = self.info['age']
        self.position = self.info['position']
