import random
import string
from requests import post
import schedule
import json


def write_pass_in_json(new_token, f_name) -> bool:
    try:
        with open(f_name, 'w', encoding='utf-8') as file:
            file.write(json.dumps({'pass_token': new_token}))
            return True
    except Exception:
        return False


def change_password():
    write_pass_in_json(''.join([random.choice(string.ascii_letters + string.digits) for _ in range(1000)]),
                       'secret_key.json')
    # print('ok')


def change_token_this():
    pass_token = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(600)])
    write_pass_in_json(pass_token, 'pass_token.json')
    if (post('http://127.0.0.1:5000/api_helper/get_new_token',
             json={'token': 'pass_api_token', 'new_token': pass_token}) and
            post('http://127.0.0.1:8080/main_helper/get_new_token',
                 json={'token': 'pass_main_token', 'new_token': pass_token})):
        # print('ok')
        pass
    else:
        change_token_this()


schedule.every(20).minutes.do(change_password)
schedule.every(15).minutes.do(change_token_this)
change_token_this()
while True:
    schedule.run_pending()
