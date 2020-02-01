#!/usr/local/bin/python3

from cgitb import enable
enable()

import pymysql as db

print('Content-Type: text/html')
print()

result = ''
try:
    connection = db.connect('localhost:8080', 'root', 'root', 'schoolify')
    cursor = connection.cursor(db.cursors.DictCursor)
    cursor.execute("""SELECT *
                      FROM users""")
    result = """<table>
                <tr><th colspan="2">Upcoming Gigs</th></tr>
                <tr><th>Band</th><th>Date</th></tr>"""
    for row in cursor.fetchall():
        result += '<tr><td>%s</td><td>%s</td></tr>' % (row['name'], row['password'])
    result += '</table>'
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
            %s
        </body>
    </html>""" % (result))