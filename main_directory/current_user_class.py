from flask_login import UserMixin
from requests import get


class User(UserMixin):
    def __init__(self, email):
        self.id = get(f'http://127.0.0.1:5000/api/users_from_email/{email}').json()['id']
