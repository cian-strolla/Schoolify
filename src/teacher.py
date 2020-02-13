#!/usr/local/bin/python3

from cgitb import enable
enable()

from cgi import FieldStorage, escape
import pymysql as db
from hashlib import sha256
from time import time
from shelve import open
from http.cookies import SimpleCookie
from os import environ
from html import escape


no_student_JSAlert=''
result = ''
student_firstname = ''
student_lastname = ''
student_phone_number=''
form_data = FieldStorage()
student_id = ''
address = ''
eircode = ''
file = ["","","",""]

cookie = SimpleCookie()
http_cookie_header = environ.get('HTTP_COOKIE')

#if cookie present
if http_cookie_header:
    cookie.load(http_cookie_header)
    #if sid cookie
    if 'sid' in cookie:
        sid = cookie['sid'].value
        session_store = open('sess_' + sid, writeback=False)
        #if authenticated cookie redirect to homepage
        if session_store['authenticated']:
            if len(form_data) != 0:
                try:
                    student_id = escape(form_data.getfirst('student_id'))
                    connection = db.connect('cs1.ucc.ie', 'rjf1', 'ahf1Aeho', '2021_rjf1')
                    cursor = connection.cursor(db.cursors.DictCursor)

                    cursor.execute("""SELECT * FROM students
                                    WHERE student_id = '%s'""" % (student_id))

                    fetched = cursor.fetchall()
                    if len(fetched)==0:
                        no_student_JSAlert='alert("Student Doesn\'t Exist. Search for a Valid Student ID.");'
                    else:
                        for row in fetched:
                            student_firstname = row['first_name']
                            student_lastname = row['last_name']
                            student_phone_number = row['phone_number']

                    cursor.close()
                    cursor = connection.cursor(db.cursors.DictCursor)

                    cursor.execute("""SELECT * FROM addresses
                                    WHERE student_id = '%s'""" % (student_id))
                    for row in cursor.fetchall():
                        address = row['address']
                        eircode = row['eircode']

                    cursor.close()
                    cursor = connection.cursor(db.cursors.DictCursor)

                    cursor.execute("""SELECT * FROM homework
                                    WHERE student_id = '%s'""" % (student_id))
                    # append all file submissions even if null
                    for row in cursor.fetchall():
                        #only possible to submit 4 files now for simplicity
                        for i in range(1,5):
                            file[0] = row['file1']
                            file[1] = row['file2']
                            file[2] = row['file3']
                            file[3] = row['file4']
                    cursor.close()
                    connection.close()
                except db.Error:
                    result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'

        else:
            print('Location: login.py')
    else:
        print('Location: login.py')
else:
    print('Location: login.py')

print('Content-Type: text/html')
print()

print("""
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">


        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
        <!-- Overriding CSS -->
        <link rel="stylesheet" href="./css/style.css">
        <link rel="icon" href="./assets/favicon.ico" type="image/x-icon">

        <!-- FontAwesome Icons -->
        <script src="https://kit.fontawesome.com/44c51e0d9c.js" crossorigin="anonymous"></script>

        <title>Schoolify</title>
      </head>
      <body>

        <script>
            function myFunction() {
                %s
            }
            myFunction()
        </script>

        <!--<div class="current-student-container container"></div>-->

        <div class="view-options container-fluid">
          <div class="row">

            <nav class="sidebar col-md-2 d-none d-md-block">


              <ul class="nav flex-column">
                <li>
                  <img src="./assets/just_logo_whiteBG.png" width="60px" height="60px">
                  <a class="#nav-link" href="#schoolify">Schoolify</a>
                </li>
                <li>
                  <!-- Search form -->
                  <form action="teacher.py" method="get">
                      <input class="form-control" type="text" name="student_id" value="%s" placeholder="Student ID" aria-label="Search" id="student_id" />
                      <input type="submit" value="Search" />
                  </form>
                </li>
                <li>
                  <!--<div class="row col-md-2" id="top-row">Student</div>               -->
                  <strong>Student: </strong>%s %s
                </li>

                <li>
                  <i class="fas fa-user-graduate"></i>
                  <a class="#nav-link" href="#personal-info">Personal Information</a>
                </li>
                <li>
                  <i class="fas fa-copy"></i>
                  <a class="#nav-link" href="#term-reports">Term Reports</a>
                </li>
                <li>
                  <i class="fas fa-clock"></i>
                  <a class="#nav-link" href="#attendance">Attendance</a>
                </li>
                <li>
                  <i class="fas fa-edit"></i>
                  <a class="#nav-link" href="#homework">Homework</a>
                </li>
                <li>
                  <i class="far fa-calendar"></i>
                  <a class="#nav-link" href="#schedule">Schedule</a>
                </li>
                <li class="logout-button">
                  <i class="fas fa-sign-out-alt"></i>
                  <a class="#nav-link" href="./logout.py">Logout</a>
                </li>
              </ul>
              </nav>
              <!--Below are the hidden content sections for the student-->
              <div class="hidden-content">
                <div class="col-md-8" id="personal-info">

                    <strong>Address: </strong> %s
                    <strong>Eircode: </strong> %s
                    <strong>Phone Number: </strong> %s
                </div>
                <div id="term-reports">
                    <p>Test2</p>
                </div>
                <div id="attendance">
                  <h1>Attendance</h1>
                  <table>
                      <tr>
                        <th>Student Name</th>
                        <th>Attendance</th>
                      </tr>
                      <tr>
                        <td>John Smith</td>
                        <td>Present</td>
                      </tr>
                      <tr>
                        <td>David Jones</td>
                        <td>Absent</td>
                      </tr>
                      <tr>
                        <td>Sally Johnson</td>
                        <td>Present</td>
                      </tr>
                      <tr>
                        <td>Michael Fitzpatrick</td>
                        <td>Present</td>
                      </tr>
                  </table>
                </div>
                <div id="homework">
						<h1>Homework</h1>
					<table>
						<tr>
							<th>Week</th>
							<th>Submission</th>
						</tr>
						<tr>
							<td>Week1</td>
							<td>%s</td>
						</tr>
						<tr>
							<td>Week2</td>
							<td>%s</td>
						</tr>
						<tr>
							<td>Week3</td>
							<td>%s</td>
						</tr>
						<tr>
							<td>Week4</td>
							<td>%s</td>
						</tr>
					</table>
              </div>
            </div>
          </div>

        <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
      </body>
    </html>
    """ % (no_student_JSAlert, student_id, student_firstname, student_lastname, address, eircode, student_phone_number, file[0], file[1], file[2], file[3]))
