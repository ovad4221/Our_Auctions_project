import datetime
from flask import jsonify
from werkzeug.security import generate_password_hash

secret_key = 'Its_a_secret_key)#Это_очень!!длинная?и+секретнаяЁЁстрокаэ/|для2343подписи^^^токена#!)0))'
# можно вообще его генерировать в функции, тогда он будет меняться постояно
hash_security = generate_password_hash(secret_key)


def make_request(data):
    return {**data, 'token': hash_security[21:]}
