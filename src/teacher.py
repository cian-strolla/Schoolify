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
teacher_name=''
form_data = FieldStorage()
student_id = ''
address = ''
eircode = ''
# HOMEWORK
homework_table =""
# POINTS
class_points_table = ''
student_specific_points = ''
points_reason = ''
points_date = ''
points_chart = ''
points = 0
points_string = ''
student_specific_points_graph = ''
student_specific_points_graph_script = ''
# SCHEDULE
current_class = ''
events_table = ''
event_date = ''
event_description = ''
event_date_input = ''
event_descrition_input = ''
event_id = ''


student_id_to_name_dict={}
attendance_list=[]
class_ids_list=[]
daily_attendance_dict=dict()
student_specific_attendance_dict={'':'', '':'', '':''}
daily_attendance_dict=student_specific_attendance_dict
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
            if session_store['account_type'] == "2":
                try:
                    current_class = session_store['class']
                    current_class = int(current_class)
                    teacher_name=session_store['name']

                    connection = db.connect('cs1.ucc.ie', 'rjf1', 'ahf1Aeho', '2021_rjf1')
                    # ATTENDANCE
                    cursor = connection.cursor(db.cursors.DictCursor)
                    cursor.execute("""SELECT * FROM students
                                            WHERE class = '1'""")
                    for row in cursor.fetchall():
                        student_id_to_name_dict[str(row['student_id'])]=row['first_name'] + " " + row['last_name']

                    cursor.close()

                    cursor = connection.cursor(db.cursors.DictCursor)
                    cursor.execute("""SELECT * FROM students
                                    WHERE class=1""")
                    for row in cursor.fetchall():
                        class_ids_list.append(row['student_id'])

                    # POINTS
                    cursor = connection.cursor(db.cursors.DictCursor)
                    cursor.execute("""SELECT * FROM points_total WHERE class=%s""" % (current_class))
                    result = current_class
                    for row in cursor.fetchall():
                        student_id = str(row['student_id'])
                        cursor2 = connection.cursor(db.cursors.DictCursor)
                        cursor2.execute("""SELECT * FROM students WHERE student_id=%s""" % (student_id))
                        for row2 in cursor2.fetchall():
                            student_firstname = row2['first_name']
                            student_lastname = row2['last_name']
                        connection.commit()
                        cursor2.close()
                        total_points = str(row['points'])
                        class_points_table += "<tr>"
                        class_points_table += "<td>" + student_firstname + " " + student_lastname + "</td>"
                        class_points_table += "<td>" + total_points + "</td>"
                        class_points_table += "</tr>"
                        points_chart +="{ y: " + total_points +", label: \"" + student_firstname + " " + student_lastname + "\" },"
                    connection.commit()
                    cursor.close()



                    # SCHEDULE
                    cursor = connection.cursor(db.cursors.DictCursor)
                    cursor.execute("""SELECT * FROM calendar WHERE class = %s ORDER BY event_date""" % (current_class))

                    for row in cursor.fetchall():
                        event_date = str(row['event_date'])
                        event_description = row['event_description']
                        event_id = str(row['id'])
                        events_table += "<tr>"
                        events_table += "<td>" + event_date + "</td>"
                        events_table += "<td>" + event_description + "</td>"
                        events_table +="""<td>
                                            <form action="deleteEvent.py" method="post">
                                                <button name="delete-button" value=\"""" + event_id + """\" class=\"delete-button" type=\"submit\">Delete</button>
                                            </form>
                                        </td>"""
                        events_table += "</tr>"
                    connection.commit()
                    cursor.close()
                    connection.close()

                except db.Error:
                    result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'

                if len(form_data) != 0:
                    try:
                        # check which input fields contain data
                        try:
                            student_id = escape(form_data.getfirst('student_id'))
                        except:
                            student_id = ''
                        try:
                            event_date_input = escape(form_data.getfirst('event-date-input'))
                        except:
                            event_date_input = ''
                        try:
                            event_descrition_input = escape(form_data.getfirst('event-description-input'))
                        except:
                            event_descrition_input = ''

                        connection = db.connect('cs1.ucc.ie', 'rjf1', 'ahf1Aeho', '2021_rjf1')

                        if student_id != '':
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


                            # POINTS
                            student_specific_points += """<div id="student-specific-points"class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
                                                            <h1 class="h2">""" + student_firstname + """\'s Points</h1>
                                                        </div>"""
                            student_specific_points += """<table class="table table-hover reasons-table">
                                                          <thead class="thead-dark">
                                                            <tr>
                                                              <th class="date" scope="col">Date</th>
                                                              <th class="event" scope="col">Reason</th>
                                                            </tr>
                                                          </thead>
                                                          <tbody>"""
                            cursor = connection.cursor(db.cursors.DictCursor)
                            cursor.execute("""SELECT * FROM points_reasons WHERE student_id = %s ORDER BY reason_date""" % (student_id))
                            for row in cursor.fetchall():
                                points_date = str(row['reason_date'])
                                points_reason = row['reason']
                                points += int(row['points'])
                                points_string = str(points)
                                student_specific_points += "<tr>"
                                student_specific_points += "<td>" + points_date + "</td>"
                                student_specific_points += "<td>" + points_reason + "</td>"
                                student_specific_points += "</tr>"
                                student_specific_points_graph_script += "{ y: " + points_string +", label: \"" + points_date + " \", },"
                            cursor.close()

                            student_specific_points += """</tbody>
                                                        </table>"""

                            student_specific_points_graph += "<div id=\"chartContainer2\"></div>"


                            # HOMEWORK
                            cursor = connection.cursor(db.cursors.DictCursor)
                                # currently using a workaround where instead of sending the eamil of teacher_name
                                # from login.py I'm using the teacher_name@gamil.com
                            teacher_email_name = teacher_name.replace(" ","")
                            cursor.execute("""SELECT * FROM homework
                                            WHERE student_id = '%s'
                                            AND teacher_email = '%s@gmail.com'""" % (student_id, teacher_email_name.lower()))

                            week =1
                                # append all file submissions even if null
                            for row in cursor.fetchall():
                                # Currently all files are in correct order so no need to use file_order atribute yet
                                # as this simplifies matters a lot
                                # Changed the file structure for where homework files will be stored to make it easier
                                homework_table += """<tr>
                                                        <td>Week %s</td>
                                                        <td><a href="homework/%s/%s" download>Solution</a></td>
                                                        <td> %s </td>
                                                        <td> %s </td>
                                                    </tr>""" % (str(week),student_id, row['filename'], str(row['result']), row['comments'])
                                week+=1
                            cursor.close()

                        # SCHEDULE
                        if event_date_input != '':
                            cursor = connection.cursor(db.cursors.DictCursor)
                            cursor.execute("""INSERT INTO `calendar` (`id`, `class`, `event_date`, `event_description`) VALUES (NULL, '%s', '%s', '%s');""" % (current_class, event_date_input, event_descrition_input))
                            connection.commit()
                            cursor.close()
                            connection.close()
                            print('Location: teacher.py#schedule')

                        connection.close()
                        # commenting this out prevents the website from being redirected to
                        # teacher.py just after entering a student id

                        # print('Location: teacher.py')

                    except db.Error:
                        result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'
            else:
                print('Location:login.py')
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
        <link href='fullcalendar/core/main.css' rel='stylesheet' />
        <link href='fullcalendar/daygrid/main.css' rel='stylesheet' />

        <!-- FontAwesome Icons -->
        <script src="https://kit.fontawesome.com/44c51e0d9c.js" crossorigin="anonymous"></script>
        <!-- Script to ensure dashboard is loaded on launch -->
        <script type="text/javascript">
            if (document.location.hash == "" || document.location.hash == "#")
                document.location.hash = "#dashboard";
        </script>

        <script src='fullcalendar/core/main.js'></script>
        <script src='fullcalendar/daygrid/main.js'></script>

        <script>

          document.addEventListener('DOMContentLoaded', function() {
            var calendarEl = document.getElementById('calendar');

            var calendar = new FullCalendar.Calendar(calendarEl, {
              plugins: [ 'dayGrid' ]
            });

            calendar.render();
          });

        </script>

        <script>
        window.onload = function () {

        var chart1 = new CanvasJS.Chart("chartContainer1", {
        	animationEnabled: true,
        	theme: "light2", // "light1", "light2", "dark1", "dark2"
        	title:{
        		text: "Student Points"
        	},
        	axisY: {
        		title: "Total Points"
        	},
        	data: [{
        		type: "column",
        		dataPoints: [
        			%s
        		]
        	}]
        });
        chart1.render();

        var chart2 = new CanvasJS.Chart("chartContainer2", {
            animationEnabled: true,
            theme: "light2",
            title:{
                text: "%s\'s Points History"
            },
            axisY:{
                includeZero: false
            },
            data: [{
                type: "line",
                dataPoints: [
                    { y: 0, label: \" \", }, %s
                ]
            }]
        });
        chart2.render();

        }
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
                          <table class="table table-hover attendance-table">
                            <thead class="thead-dark">
                              <tr>
                                <th scope="col">#</th>
                                <th scope="col">Student Name</th>
                                <th scope="col">Attendance</th>
                              </tr>
                            </thead>
                            <tbody>
                              <tr>
                                <th scope="row">1</th>
                                <td>%s</td>
                                <td>%s</td>
                              </tr>
                              <tr>
                                <th scope="row">2</th>
                                <td>%s</td>
                                <td>%s</td>
                              </tr>
                              <tr>
                                <th scope="row">3</th>
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
                        <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
                            <h1 class="h2">Points</h1>
                        </div>
                        <table class="table table-hover points-table">
                          <thead class="thead-dark">
                            <tr>
                              <th class="student-name" scope="col">Student Name</th>
                              <th class="student-points" scope="col">Points Accumulated</th>
                            </tr>
                          </thead>
                          <tbody>
                            %s
                          </tbody>
                        </table>
                        %s
                        <div id="chartContainer1"></div>
                        <script src="https://canvasjs.com/assets/script/canvasjs.min.js"></script>
                        %s
                    </div>
                    <div id="homework">
    					<div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
                            <h1 class="h2">Homework</h1>
                        </div>
    					<table>
    						<tr>
    							<th>Week</th>
    							<th>Submission</th>
                                <th>Result</th>
                                <th>Comments</th>
    						</tr>

    						<!-- creating these table rows dynamically now so that more rows can be added when needed-->
                            %s

    					</table>
                    </div>
                    <div id="schedule">
                        <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
                            <h1 class="h2">Schedule</h1>
                        </div>
                        <div id='calendar'></div>

                        <div class="event-input">
                        <form action="teacher.py" method="post" class="event-input-form">
                            <h1>Create an Event</h1>
                            <label for="event-date-input" class="sr-only">Event Date</label>
                            <input name="event-date-input" type="text" id="event-date-input" class="form-control" placeholder="YYYY-MM-DD" required autofocus>
                            <label for="event-description-input" class="sr-only">Description</label>
                            <input name="event-description-input"type="text" id="event-description-input" class="form-control" placeholder="Description" required>
                            <button class="landing btn btn-lg btn-primary btn-block" type="submit">Create Event</button>
                        </form>
                        </div>


                        <div id="events-schedule">
                            <table class="table table-hover events-table">
                              <thead class="thead-dark">
                                <tr>
                                  <th class="date" scope="col">Date</th>
                                  <th class="event" scope="col">Event</th>
                                  <th class="delete-button" scope="col"></th>
                                </tr>
                              </thead>
                              <tbody>
                                %s
                            </tbody>
                            </table>
                            %s
                        </div>
                    </div>
                </div>
              </main>
            </div>
          </div>

        <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
      </body>
    </html>
    """ % (points_chart, student_firstname, student_specific_points_graph_script, no_student_JSAlert, student_id, student_firstname, student_lastname,\
    teacher_name, \
     list(daily_attendance_dict.keys())[0], list(daily_attendance_dict.values())[0],\
     list(daily_attendance_dict.keys())[0], list(daily_attendance_dict.values())[0],\
     list(daily_attendance_dict.keys())[0], list(daily_attendance_dict.values())[0],\
      address, eircode, student_phone_number,\
      student_firstname, student_lastname, \
      list(student_specific_attendance_dict.keys())[0], list(student_specific_attendance_dict.values())[0],\
      list(student_specific_attendance_dict.keys())[0], list(student_specific_attendance_dict.values())[0],\
      list(student_specific_attendance_dict.keys())[0], list(student_specific_attendance_dict.values())[0],\
      class_points_table, student_specific_points, student_specific_points_graph, homework_table, events_table, result))
