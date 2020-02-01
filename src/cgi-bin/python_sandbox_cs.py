#!/usr/local/bin/python3

from cgitb import enable
enable()

import pymysql as db

print('Content-Type: text/html')
print()

result = ''
try:
    connection = db.connect('cs1.ucc.ie', 'rjf1', 'ahf1Aeho', '2021_rjf1')
    cursor = connection.cursor(db.cursors.DictCursor)

    cursor.execute("""SELECT *
                      FROM users""")
    result = """"""
    for row in cursor.fetchall():
        result += '<p>%s</p>' % (row['username'])
    #result += '</table>'
    cursor.close()
    connection.close()
except db.Error:
    result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'

print("""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8" />
            <title>Upcoming Gigs</title>
        </head>
        <body>
            <p>Test</p>
            %s
        </body>
    </html>""" % (result))