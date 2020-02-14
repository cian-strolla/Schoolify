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
# PERSONAL IFNO
student_firstname = ''
student_lastname = ''
student_phone_number=''

form_data = FieldStorage()
student_id = ''
address = ''
eircode = ''
# HOMEWORK
file = ["","","",""]
# POINTS
weekly=''
monthly=''
yearly=''
x=''


student_id_to_name_dict={}
attendance_list=[]
class_ids_list=[]
daily_attendance_dict=dict()
student_specific_attendance_dict={'select':'student', 'select':'student', 'select':'student'}
simple=''
presence_dict=dict()

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
            try:
                connection = db.connect('cs1.ucc.ie', 'rjf1', 'ahf1Aeho', '2021_rjf1')
                cursor = connection.cursor(db.cursors.DictCursor)
                cursor.execute("""SELECT * FROM students
                                        WHERE class = '1'""")
                for row in cursor.fetchall():
                    student_id_to_name_dict[str(row['student_id'])]=row['first_name'] + " " + row['last_name']

                cursor.close()

                cursor = connection.cursor(db.cursors.DictCursor)
                cursor.execute("""SELECT * FROM attendance
                                        WHERE date='2020-02-07' and class=1""") #% (now.strftime("%Y-%m-%d")))

                for row in cursor.fetchall():
                    for student in ['student_1', 'student_2', 'student_3']:
                        x = row[student].split()
                        if x[1] == '1':
                            x[1]='Present'
                        elif x[1] == '0':
                            x[1]='Absent'
                        daily_attendance_dict[student_id_to_name_dict[x[0]]]=x[1]
                cursor.close()
                cursor = connection.cursor(db.cursors.DictCursor)
                cursor.execute("""SELECT * FROM students
                                WHERE class=1""")
                for row in cursor.fetchall():
                    class_ids_list.append(row['student_id'])
                cursor.close()

            except db.Error:
                result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'

            if len(form_data) != 0:
                try:
                    student_id = escape(form_data.getfirst('student_id'))
                    connection = db.connect('cs1.ucc.ie', 'rjf1', 'ahf1Aeho', '2021_rjf1')

                    # PERSONAL INFO
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


                    # ATTENDANCE
                    cursor = connection.cursor(db.cursors.DictCursor)
                    cursor.execute("""SELECT * FROM attendance
                                    WHERE class=1 and date between '2020-02-05' and '2020-02-07'""")
                    for row in cursor.fetchall():
                        for student in ['student_1', 'student_2', 'student_3']:
                            x = row[student].split()
                            if x[0] == student_id:
                                if x[1] == '1':
                                    x[1]='Present'
                                elif x[1] == '0':
                                    x[1]='Absent'
                                student_specific_attendance_dict[row['date']]=x[1]


                            #daily_attendance_dict[student_id_to_name_dict[x[0]]]=x[1]

                    cursor.close()


                    # POINTS
                    cursor = connection.cursor(db.cursors.DictCursor)
                    cursor.execute("""SELECT * FROM points
                                    WHERE student_id = '%s'""" % (student_id))
                    for row in cursor.fetchall():
                        weekly=row['weekly']
                        monthly=row['monthly']
                        yearly=row['yearly']
                    cursor.close()

                    # HOMEWORK
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
        <!-- Script to ensure dashboard is loaded on launch -->
        <script type="text/javascript">
            if (document.location.hash == "" || document.location.hash == "#")
                document.location.hash = "#dashboard";
        </script>
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
                  <a class="#nav-link" href="#dashboard">Schoolify</a>
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
                  Student: <strong>%s %s</strong>
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
                  <i class="fas fa-chart-bar"></i>
                  <a class="#nav-link" href="#points">Points</a>
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
              <main role="main" class="col-md-9 ml-sm-auto col-lg-10 pt-3 px-4">

                  <!--Below are the hidden content sections for the student-->
                  <div class="hidden-content">
                    <div id="dashboard">
                          <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
                              <h1 class="h2">Dashboard</h1>
                          </div>
                          <p>Welcome back %s</p>
                          <h1>Class Attendance</h1>
                          <table>
                              <tr>
                                <th>Student Name</th>
                                <th>Attendance</th>
                              </tr>
                              <tr>
                                <td>%s</td>
                                <td>%s</td>
                              </tr>
                              <tr>
                                <td>%s</td>
                                <td>%s</td>
                              </tr>
                              <tr>
                                <td>%s</td>
                                <td>%s</td>
                              </tr>
                          </table>
                    </div>
                    <div class="col-md-8" id="personal-info">

                        <strong>Address: </strong> %s
                        <strong>Eircode: </strong> %s
                        <strong>Phone Number: </strong> %s
                    </div>
                    <div id="term-reports">
                        <p>Test2</p>
                    </div>
                    <div id="attendance">
                      <h1>Attendance for %s %s</h1>
                      <table>
                          <tr>
                            <th>Date</th>
                            <th>Attendance</th>
                          </tr>
                          <tr>
                            <td>%s</td>
                            <td>%s</td>
                          </tr>
                          <tr>
                            <td>%s</td>
                            <td>%s</td>
                          </tr>
                          <tr>
                            <td>%s</td>
                            <td>%s</td>
                          </tr>

                      </table>
                    </div>
                    <div id="points">
                        <p>Weekly: %s</p>
                        <p>Monthly: %s</p>
                        <p>Yearly: %s</p>
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
                  </main>
            </div>
          </div>

        <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
      </body>
    </html>
    """ % (no_student_JSAlert, student_id, student_firstname, student_lastname,\
    session_store['name'], \
     list(daily_attendance_dict.keys())[0], list(daily_attendance_dict.values())[0],\
     list(daily_attendance_dict.keys())[1], list(daily_attendance_dict.values())[1],\
     list(daily_attendance_dict.keys())[2], list(daily_attendance_dict.values())[2],\
      address, eircode, student_phone_number,\
      student_firstname, student_lastname, \
      list(student_specific_attendance_dict.keys())[0], list(student_specific_attendance_dict.values())[0],\
      list(student_specific_attendance_dict.keys())[1], list(student_specific_attendance_dict.values())[1],\
      list(student_specific_attendance_dict.keys())[2], list(student_specific_attendance_dict.values())[2],\
      weekly, monthly, yearly, \
      file[0], file[1], file[2], file[3]))
