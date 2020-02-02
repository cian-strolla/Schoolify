#!/usr/local/bin/python3

from cgitb import enable
enable()

from cgi import FieldStorage
from html import escape
import pymysql as db

print('Content-Type: text/html')
print()

form_data = FieldStorage()
bandname = ''
result = ''
if len(form_data) != 0:
    try:
        student_id = escape(form_data.getfirst('bandname'))
        connection = db.connect('cs1.ucc.ie', 'rjf1', 'ahf1Aeho', '2021_rjf1')
        cursor = connection.cursor(db.cursors.DictCursor)
        cursor.execute("""SELECT * FROM students
                          WHERE student_id = '%s'""" % (student_id))
        result = """<table>
                    <tr><th>Gig Dates</th></tr>"""
        for row in cursor.fetchall():
            result += '<tr><td>%s</td></tr>' % row['first_name']
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
            <title>Gigs by band</title>
        </head>
        <body>
            <form action="band_gigs.py" method="get">
                <label for="bandname">Band: </label>
                <input type="text" name="bandname" vale="%s" size="50" maxlength="50" id="bandname" />
                <input type="submit" value="Search for gigs" />
            </form>
            %s
        </body>
    </html>""" % (bandname, result))