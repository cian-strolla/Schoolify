#!/usr/local/bin/python3

from cgitb import enable
enable()

from cgi import FieldStorage, escape
import pymysql as db
from hashlib import sha256
from datetime import date
from shelve import open
from http.cookies import SimpleCookie
from os import environ
from html import escape
import cgi, cgitb

testing = ''
no_student_JSAlert=''
result = ''
today=date.today()
# PERSONAL IFNO
student_firstname = ''
student_lastname = ''
parent_firstname = ''
parent_lastname = ''
contact_number=''
teacher_name=' '
form_data = FieldStorage()
student_id = ''
address = ''
eircode = ''
personal_info = ''
date_of_birth = ''
# HOMEWORK
homework_table =""
# POINTS
class_points_table = ''
student_specific_points = ''
points_reason = ''
points_date = ''
points_chart = ''
points = 0
points_total = 0
points_string = ''
student_specific_points_graph = ''
student_specific_points_graph_script = ''
points_id_input = ''
points_input = ''
points_reason_input = ''

# SCHEDULE
current_class = ''
events_table = ''
event_date = ''
event_description = ''
event_date_input = ''
event_descrition_input = ''
event_id = ''
'default'
attendance_table=''
attendance_taken=False
x=''

student_id_to_name_dict={}
attendance_list=[]
class_ids_list=[]
daily_attendance_dict=dict()
student_specific_attendance_dict={'2020-02-05':'no student selected', '2020-02-06':'no student selected', '2020-02-07':'no student selected'}
#daily_attendance_dict=student_specific_attendance_dict
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
                    teacher_name=session_store['name']
                    current_class = session_store['class']
                    #current_class = int(current_class)

                    connection = db.connect('cs1.ucc.ie', 'rjf1', 'ahf1Aeho', '2021_rjf1')
                    # PERSONAL INFO
                    cursor = connection.cursor(db.cursors.DictCursor)
                    cursor.execute("""SELECT * FROM students where class=%s"""% current_class)

                    for row in cursor.fetchall():
                        student_id = str(row['student_id'])
                        student_firstname = row['first_name']
                        student_lastname = row['last_name']

                        cursor2 = connection.cursor(db.cursors.DictCursor)
                        cursor2.execute("""SELECT * FROM parents where child1=%s or child2=%s or child3=%s or child4=%s"""% (student_id,student_id,student_id,student_id))
                        for row2 in cursor2.fetchall():
                            parent_firstname = row2['first_name']
                            parent_lastname = row2['last_name']
                        cursor2.close()

                        cursor3 = connection.cursor(db.cursors.DictCursor)
                        cursor3.execute("""SELECT * FROM addresses WHERE student_id=%s"""% student_id)
                        for row3 in cursor3.fetchall():
                            address = row3['address']
                            eircode = row3['eircode']
                        cursor3.close()

                        date_of_birth = str(row['date_of_birth'])
                        contact_number = str(row['phone_number'])
                        personal_info += "<tr>"
                        personal_info += "<td>" + student_firstname + " " + student_lastname + "</td>"
                        personal_info += "<td>" + parent_firstname + " " + parent_lastname +"</td>"
                        personal_info += "<td>" + date_of_birth + "</td>"
                        personal_info += "<td>" + address + "</td>"
                        personal_info += "<td>" + eircode + "</td>"
                        personal_info += "<td>" + contact_number + "</td>"
                        events_table += "</tr>"
                    connection.commit()
                    cursor.close()

                    # ATTENDANCE
                    cursor = connection.cursor(db.cursors.DictCursor)
                    cursor.execute("""SELECT * FROM students
                                            WHERE class = '1'""")
                    for row in cursor.fetchall():
                        student_id_to_name_dict[str(row['student_id'])]=row['first_name'] + " " + row['last_name']

                    cursor.close()

                    # CLASS ID'S
                    cursor = connection.cursor(db.cursors.DictCursor)
                    cursor.execute("""SELECT student_ids FROM classes
                                WHERE id=1""")

                    class_ids_list=cursor.fetchone()['student_ids'].split()
                    cursor.close()


                    # CLASS ATTENDANCE
                    cursor = connection.cursor(db.cursors.DictCursor)
                    cursor.execute("""SELECT attendance FROM attendance
                                WHERE class=1 and date='2020-02-14'""")
                    fetched=cursor.fetchone()
                    if(fetched==None):

                        cursor.close()
                        cursor = connection.cursor(db.cursors.DictCursor)
                        cursor.execute("""INSERT INTO attendance
                                    VALUES('2020-02-14', 1, '222')""")
                        connection.commit()
                        cursor.close()

                    else:

                        attendance_list= list(fetched['attendance'])
                        for i in range(0, len(attendance_list)):
                            if attendance_list[i]=='0':
                                attendance_taken=True
                                daily_attendance_dict[student_id_to_name_dict[class_ids_list[i]]]='Absent'
                            elif attendance_list[i]=='1':
                                attendance_taken=True
                                daily_attendance_dict[student_id_to_name_dict[class_ids_list[i]]]='Present'
                            elif attendance_list[i]=='2':
                                daily_attendance_dict[student_id_to_name_dict[class_ids_list[i]]]='Attendance Not Taken'

                    cursor.close()

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

                    student_firstname = ''
                    student_lastname = ''
                    student_id = ''

                    # Discussion

                    printer = ""
                    counter = 0
                    teacher_id = session_store['id']
                    parentfname = []
                    cursor3 = connection.cursor(db.cursors.DictCursor)
                    cursor3.execute("SELECT * FROM parents")

                    for row in cursor3.fetchall():
                        parentfname.append(row['first_name'])
                    cursor3.close()

                    parentfname = ['Ben', 'Rachel', 'Nora']

                    cursor = connection.cursor(db.cursors.DictCursor)

                    cursor.execute("""SELECT * FROM discussion_board WHERE sender_id = %s OR receiver_id = %s""" % (teacher_id, teacher_id))

                    for row in cursor.fetchall():
                        counter += 1
                        sender_id = row['sender_id']
                        receiver_id = row["receiver_id"]
                        cursor2 = connection.cursor(db.cursors.DictCursor)
                        cursor2.execute("SELECT * FROM parents WHERE id = %s" % (receiver_id))

                        for row in cursor2.fetchall():
                            parent_firstname = row["first_name"]
                        cursor2.close()

                        if counter > len(parentfname):
                            printer += ""
                        else:
                            printer += "<tr>"
                            printer += "<td>"
                            printer += parentfname[counter-1]
                            printer += "</td>"
                            printer += "<td>"
                            printer += "<button class='discussion_buttons' onclick='displayDiscussion(%s)'>Click to open</button>" % (counter)
                            printer += "</td>"
                            printer += "</tr>"
                        printer += "<p hidden id=sender_id+%s>%s</p>" % (counter, sender_id)
                        printer += "<p hidden id=receiver_id+%s>%s</p>" % (counter, receiver_id)
                    connection.commit()
                    cursor.close()
                    connection.close()


                except db.Error:
                    result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'

                teacher_email_name = teacher_name.replace(" ","")
                teacher_email_name = teacher_email_name.lower()

                if len(form_data) != 0:

                    try:
                        # check which input fields contain data
                        # and from with source, i.e. from searching or from adding event
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
                        try:
                            student_1_attendance = escape(form_data.getfirst('optradio1'))
                        except:
                            student_1_attendance = '2'
                        try:
                            student_2_attendance = escape(form_data.getfirst('optradio2'))
                        except:
                            student_2_attendance = '2'
                        try:
                            student_3_attendance = escape(form_data.getfirst('optradio3'))
                        except:
                            student_3_attendance = '2'
                        try:
                            file_upload = escape(form_data.getfirst('filename'))
                        except:
                            file_upload = ''
                        try:
                            points_id_input = escape(form_data.getfirst('points-id-input'))
                        except:
                            points_id_input = ''
                        try:
                            points_input = escape(form_data.getfirst('points-input'))
                        except:
                            points_input = ''
                        try:
                            points_reason_input = escape(form_data.getfirst('points-reason-input'))
                        except:
                            points_reason_input = ''
                        try:
                            if file_upload.has_key('filename'):
                                file_upload = form_data['filename'].file
                            #file_upload = form['filename']
                        except:
                            file_upload = 'failed'


                        # UPDATE ATTENDANCE

                        connection = db.connect('cs1.ucc.ie', 'rjf1', 'ahf1Aeho', '2021_rjf1')

                        cursor = connection.cursor(db.cursors.DictCursor)
                        cursor.execute("""UPDATE attendance
                                    SET attendance=%s WHERE date='2020-02-14'""" % (student_1_attendance+student_2_attendance+student_3_attendance))
                        connection.commit()
                        cursor.close()

                        if student_id != '':

                            # PERSONAL INFO
                            personal_info = ''
                            cursor = connection.cursor(db.cursors.DictCursor)
                            cursor.execute("""SELECT * FROM students
                                            WHERE student_id = %s""" % (student_id))
                            fetched = cursor.fetchall()
                            if len(fetched)==0:
                                no_student_JSAlert='alert("Student Doesn\'t Exist. Search for a Valid Student ID.");'
                            else:
                                for row in fetched:
                                    student_id = str(row['student_id'])
                                    student_firstname = row['first_name']
                                    student_lastname = row['last_name']

                                    cursor2 = connection.cursor(db.cursors.DictCursor)
                                    cursor2.execute("""SELECT * FROM parents where child1=%s or child2=%s or child3=%s or child4=%s"""% (student_id,student_id,student_id,student_id))
                                    for row2 in cursor2.fetchall():
                                        parent_firstname = row2['first_name']
                                        parent_lastname = row2['last_name']
                                    cursor2.close()

                                    cursor3 = connection.cursor(db.cursors.DictCursor)
                                    cursor3.execute("""SELECT * FROM addresses WHERE student_id=%s"""% student_id)
                                    for row3 in cursor3.fetchall():
                                        address = row3['address']
                                        eircode = row3['eircode']
                                    cursor3.close()

                                    date_of_birth = str(row['date_of_birth'])
                                    contact_number = str(row['phone_number'])
                                    personal_info += "<tr>"
                                    personal_info += "<td>" + student_firstname + " " + student_lastname + "</td>"
                                    personal_info += "<td>" + parent_firstname + " " + parent_lastname +"</td>"
                                    personal_info += "<td>" + date_of_birth + "</td>"
                                    personal_info += "<td>" + address + "</td>"
                                    personal_info += "<td>" + eircode + "</td>"
                                    personal_info += "<td>" + contact_number + "</td>"
                                    events_table += "</tr>"
                                connection.commit()
                            cursor.close()


                            # STUDENT-SPECIFIC ATTENDANCE
                            student_index=0
                            for i in range(len(class_ids_list)):

                                if class_ids_list[i]==str(student_id):
                                    student_index=i
                            x=student_index
                            cursor = connection.cursor(db.cursors.DictCursor)

                            cursor.execute("""SELECT * FROM attendance
                                            WHERE class=1 and date between '2020-02-05' and '2020-02-07'""")

                            # clear the dictionary for new entries
                            student_specific_attendance_dict.clear()
                            for row in cursor.fetchall():
                                if list(row['attendance'])[student_index]=='1':
                                    student_specific_attendance_dict[row['date']]='Present'
                                elif list(row['attendance'])[student_index]=='0':
                                    student_specific_attendance_dict[row['date']]='Absent'
                                else:
                                    student_specific_attendance_dict[row['date']]='N/A'


                            cursor.close()


                            # STUDENT_SPECIFIC POINTS
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
                            cursor.execute("""SELECT * FROM homework
                                            WHERE student_id = '%s'
                                            AND teacher_email = '%s@gmail.com'""" % (student_id, teacher_email_name))

                            week =1
                                # append all file submissions even if null
                            for row in cursor.fetchall():
                                # Currently all files are in correct order so no need to use file_order atribute yet
                                # as this simplifies matters a lot
                                # Changed the file structure for where homework files will be stored to make it easier
                                homework_table += """<tr>
                                                        <td>Week %s</td>
                                                        <td><a href="tests/%s/%s" download>Solution</a></td>
                                                        <td> %s </td>
                                                        <td> %s </td>
                                                    </tr>""" % (str(week),student_id, row['filename'], str(row['result']), row['comments'])
                                week+=1
                            cursor.close()

                        # POINTS
                        if points_input != '':
                            cursor = connection.cursor(db.cursors.DictCursor)
                            cursor.execute("""INSERT INTO `points_reasons` (`student_id`, `reason_date`, `reason`, `points`, `class`) VALUES ('%s', '%s', '%s', '%s', '%s')""" % (points_id_input,today,points_reason_input,points_input,current_class))
                            connection.commit()
                            cursor.execute("""SELECT * FROM points_total WHERE student_id=%s""" % points_id_input)
                            if cursor.rowcount != 0:
                                for row in cursor.fetchall():
                                    points_total = int(row['points'])
                                    points_total += int(points_input)
                                    testing = "ngiejfivbf"
                                cursor.execute("""UPDATE points_total SET points=%s WHERE student_id=%s""" % (points_total, points_id_input))
                                connection.commit()
                            cursor.close()
                            print('Location: teacher.py#points')

                        # SCHEDULE
                        if event_date_input != '':
                            cursor = connection.cursor(db.cursors.DictCursor)
                            cursor.execute("""INSERT INTO `calendar` (`id`, `class`, `event_date`, `event_description`) VALUES (NULL, '%s', '%s', '%s');""" % (current_class, event_date_input, event_descrition_input))
                            connection.commit()
                            cursor.close()
                            connection.close()
                            print('Location: teacher.py#schedule')

                        # commenting this out prevents the website from being redirected to
                        # teacher.py just after entering a student id

                        # print('Location: teacher.py')

                        # HOMEWORK
                        if file_upload != '':
                            try:
                                result_mark = escape(form_data.getfirst('result'))
                            except:
                                result_mark = ''
                            try:
                                comment = escape(form_data.getfirst('comments'))
                            except:
                                comment = ''
                            try:
                                student_hw_id = escape(form_data.getfirst('student-id'))
                            except:
                                student_hw_id = student_id
                            cursor = connection.cursor(db.cursors.DictCursor)
                            cursor.execute("""SELECT COUNT(*) FROM homework""")
                            for row in cursor.fetchall():
                                row_count = row['COUNT(*)']
                            test2 = """INSERT INTO homework (homework_id, teacher_email, student_id, filename, file_order, result, comments)
                                            VALUES (4, '%s@gmail.com', %s, '%s', 4, %s, '%s');""" % (teacher_email_name, student_hw_id, file_upload, result_mark, comment)
                            cursor.execute("""INSERT INTO homework (homework_id, teacher_email, student_id, filename, file_order, result, comments)
                                            VALUES (%d, '%s@gmail.com', %s, '%s', 4, %s, '%s');""" % (int(row_count)+1,teacher_email_name, student_hw_id, file_upload, result_mark, comment))
                            connection.commit()
                            cursor.close()
                            connection.close()
                            print("Location: teacher.py?student_id=%s#tests" % (student_hw_id))

                        connection.close()


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
if not attendance_taken:
    attendance_table=attendance_table="""<h1>Take Daily Attendance</h1>
    <form action="teacher.py" onsubmit="post();return false;">
    <table class="table table-hover">
      <thead class="thead-dark">
        <tr>
          <th scope="col">#</th>
          <th scope="col">Student Name</th>
          <th scope="col">Present</th>
          <th scope="col">Absent</th>
        </tr>
      </thead>
      <tbody>

        <tr>
          <th scope="row">1</th>
          <td>%s</td>
          <td><input type="radio" name="optradio1" value="1"></td>
          <td><input type="radio" name="optradio1" value="0"></td>
        </tr>
        <tr>
          <th scope="row">2</th>
          <td>%s</td>
          <td><input type="radio" name="optradio2" value="1"></td>
          <td><input type="radio" name="optradio2" value="0"></td>
        </tr>
        <tr>
          <th scope="row">3</th>
          <td>%s</td>
          <td><input type="radio" name="optradio3" value="1"></td>
          <td><input type="radio" name="optradio3" value="0"></td>
        </tr>

        </tbody>
      </table>
      <input type="submit" value="Submit" />


      </form>""" % (student_id_to_name_dict[class_ids_list[0]],\
      student_id_to_name_dict[class_ids_list[1]],\
      student_id_to_name_dict[class_ids_list[2]])

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
        <script src="canvasjs.min.js"></script>

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
                title: "Total Points",
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

        <script>
            function displayDiscussion(checker) {
                get_sender = 'sender_id+' + checker
                get_receiver = 'receiver_id+' + checker
                var sender_id = document.getElementById(get_sender).innerHTML;
                var receiver_id = document.getElementById(get_receiver).innerHTML;
                xmlhttp = new XMLHttpRequest();
                xmlhttp.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {
                        document.getElementById("current_discussion").innerHTML = this.responseText;
                    }
                };
                xmlhttp.open("GET","get_discussion.php?q="+sender_id+"&k="+receiver_id,true);
                xmlhttp.send();
            }
        </script>


        <!--<div class="current-student-container container"></div>-->

        <div class="view-options container-fluid">
          <div class="row">

            <nav class="sidebar col-md-2 d-none d-md-block">

              <ul class="nav flex-column">
                <li>
                  <img src="./assets/just_logo_whiteBG.png" width="60px" height="60px">
                  <a class="#nav-link" href="teacher.py">Schoolify</a>
                </li>

                <!--Search Form-->
                <li class="search_bar">
                    <form class="form-inline d-flex justify-content-center md-form form-sm mt-0" action="teacher.py" method="get">
                        <i class="fas fa-search" aria-hidden="true"></i>
                        <input class="form-control form-control-sm ml-3 w-75" name="student_id" value="%s" type="text" placeholder="Student ID" aria-label="Search">
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
                  <i class="fas fa-clock"></i>
                  <a class="#nav-link" href="#attendance">Attendance</a>
                </li>
                <li>
                  <i class="fas fa-chart-bar"></i>
                  <a class="#nav-link" href="#points">Points</a>
                </li>
                <li>
                  <i class="fas fa-edit"></i>
                  <a class="#nav-link" href="#tests">Tests</a>
                </li>
                <li>
                  <i class="far fa-calendar"></i>
                  <a class="#nav-link" href="#schedule">Schedule</a>
                </li>
                <li>
                    <i class="far fa-comment-dots"></i>
                    <a class="#nav-link" href="#discussion">Discussion Board</a>
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
                              <h1 class="h2">Dashboard<p id="date">%s</p></h1>

                              <div class="align-items-end profile-header-container">
    		                    <div class="profile-header-img">
                                    <img class="img-circle" src="./assets/teacher/5.jpg" />
                                </div>
                               </div>
                          </div>
                          <p>Welcome back %s</p>
                          <h1>Class Attendance</h1>
                          <table class="table table-hover">
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
                             </tbody>
                            </table>

                            <!-- TAKE ATTENDANCE TABLE -->
                            %s


                    </div>
                    <div class="col-md-8" id="personal-info">
                        <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
                            <h1 class="h2">Personal Information</h1>
                        </div>
                        <table class="table table-hover personal-info-table">
                          <thead class="thead-dark">
                            <tr>
                              <th class="date" scope="col">Student</th>
                              <th class="event" scope="col">Parent</th>
                              <th class="event" scope="col">DOB</th>
                              <th class="event" scope="col">Address</th>
                              <th class="event" scope="col">Eircode</th>
                              <th class="event" scope="col">Contact Number</th>
                            </tr>
                          </thead>
                          <tbody>
                            %s
                        </tbody>
                        </table>
                    </div>


                    <div id="attendance">
                        <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
                            <h1 class="h2">Attendance for %s %s</h1>
                        </div>

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
                            <h1 class="h2">Class Points</h1>
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
                        <div class="points-input">
                        <form action="teacher.py" method="post" class="points-input-form">
                            <h1>Give Points</h1>
                            <label for="points-id-input" class="sr-only">Student ID</label>
                            <input name="points-id-input" type="text" id="points-id-input" class="form-control" placeholder="Student-ID" required autofocus>
                            <label for="points-reason-input" class="sr-only">Reason</label>
                            <input name="points-reason-input" type="text" id="points-reason-input" class="form-control" placeholder="Reason" required autofocus>
                            <label for="points-input" class="sr-only">Points</label>
                            <input name="points-input"type="text" id="points-input" class="form-control" placeholder="Points" required>
                            <button class="landing btn btn-lg btn-primary btn-block" type="submit">Give Points</button>
                        </form>
                        </div>
                        %s
                        <div id="chartContainer1"></div>
                        %s
                    </div>

                    <div id="tests">
    					<div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
                            <h1 class="h2">Tests</h1>
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
                        <p></p>
                        <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
                            <h1 class="h2">Upload Test</h1>
                        </div>
                        <table>
                            <tr>
                                <th>Submission</th>
                                <th>Result</th>
                                <th>Comment</th>
                                <th>Student</th>
                                <th>Submit</th>
                            </tr>
                            <form enctype="multipart/form-data" action="teacher.py" method="post">
								<td>File: <input type="file" name="filename" /></td>
								<td><input type="text" id="result" class="result" name="result"/></td>
								<td><input type="text" id="comments" name="comments"/></td>
								<td><input type="text" id="student_id" class="student-id" name="student-id" value="%s"/></td>
								<td><input type="submit" value="upload" /></p></td>
							</form>
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
                    <div id="discussion">
                        <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
                            <h1 class="h2">Discussion Board</h1>
                        </div>
                        <div id="conversations">
                            <table id='discussion_beginning'>
                                <thead class="thead-dark">
                                    <tr>
                                        <th class="active_conversations" scope="col">Active Conversations</th>
                                        <th class="visit_conversation" scope="col">Visit Conversation</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    %s
                                </tbody>
                            </table>
                            <div id="send_message">
                                <p>Please choose a recipient: </p>
                                <form class="parent_to_send_" id="parent_to_send_" action="send_message.py" method="post">
                                  <input type="radio" id="parent1" name="parent" value="70">
                                  <label for="parent1">Ben</label><br>
                                  <input type="radio" id="parent2" name="parent" value="50">
                                  <label for="parent2">Rachel</label><br>
                                  <input type="radio" id="parent3" name="parent" value="60">
                                  <label for="parent3">Nora</label><br><br>
                                  <input type="submit" value="Send Message">
                                </form>
                                <textarea id="message_text_area" form="parent_to_send_" rows="3" cols="50" name="message_to_send" placeholder="Enter a message to send here..."></textarea>
                                
                            </div>
                            <div>
                                <p id="current_discussion"></p>
                            </div>
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
    today, teacher_name,\
     list(daily_attendance_dict.keys())[0], list(daily_attendance_dict.values())[0],\
     list(daily_attendance_dict.keys())[1], list(daily_attendance_dict.values())[1],\
     list(daily_attendance_dict.keys())[2], list(daily_attendance_dict.values())[2],\
     attendance_table, personal_info, \
      student_firstname, student_lastname,\
      list(student_specific_attendance_dict.keys())[0], list(student_specific_attendance_dict.values())[0],\
      list(student_specific_attendance_dict.keys())[1], list(student_specific_attendance_dict.values())[1],\
      list(student_specific_attendance_dict.keys())[2], list(student_specific_attendance_dict.values())[2],\
      class_points_table, student_specific_points, student_specific_points_graph, homework_table, student_id, events_table, points_id_input, printer))
