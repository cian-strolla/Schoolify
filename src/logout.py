#!/usr/local/bin/python3

from cgitb import enable
enable()

from cgi import FieldStorage, escape
import pymysql as db
from hashlib import sha256
from shelve import open
from http.cookies import SimpleCookie
from os import environ
from html import escape

cookie = SimpleCookie()
http_cookie_header = environ.get('HTTP_COOKIE')

#if cookie present
if http_cookie_header:
    cookie.load(http_cookie_header)
    #if sid cookie
    if 'sid' in cookie:
        sid = cookie['sid'].value
        session_store = open('sess_' + sid, writeback=False)
        #unauthenticate cookie
        session_store['authenticated'] = False
print('Location: login.py')

print('Content-Type: text/html')
print()
