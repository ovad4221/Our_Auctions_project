from requests import get


def make_request(data):
    return {**data,
            'token': get('http://127.0.0.1:4010/get_password', json={'password_check': 'cock'}).json()[
                'token']}
