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
form_data = FieldStorage()
event_id = ''

event_id = str(escape(form_data.getfirst('delete-button')))

#if cookie present
if http_cookie_header:
    cookie.load(http_cookie_header)
    #if sid cookie
    if 'sid' in cookie:
        sid = cookie['sid'].value
        session_store = open('sess_' + sid, writeback=False)
        #if authenticated cookie redirect to homepage
        if session_store['authenticated']:
            if session_store['account_type'] == "2":
                try:
                    connection = db.connect('cs1.ucc.ie', 'rjf1', 'ahf1Aeho', '2021_rjf1')
                    cursor = connection.cursor(db.cursors.DictCursor)
                    cursor.execute("""DELETE FROM `calendar` WHERE `id` = '%s';""" % (event_id))
                    connection.commit()
                    cursor.close()
                    connection.close()
                except db.Error:
                    result = "<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>"

print('Location: teacher.py')

print('Content-Type: text/html')
print()
