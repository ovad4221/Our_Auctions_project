from requests import get


def make_request(data):
    return {**data,
            'token': get('http://127.0.0.1:4010/get_password', json={'password_check': 'cock'}).json()[
                'token']}


def money_in_rubles(string):
    value_ta = string.split()
    # print(value_ta)
    if value_ta[2][1:-1] == 'RUB':
        # print(float(value_ta[0]))
        return float(value_ta[0])
    response = get('https://www.cbr-xml-daily.ru/daily_json.js')
    if response:
        resp_js = response.json()
        # print(resp_js["Valute"][value_ta[2][1:-1]]['Value'] * float(value_ta[0]))
        try:
            return resp_js["Valute"][value_ta[2][1:-1]]['Value'] * float(value_ta[0])
        except Exception as e:
            return str(e)
