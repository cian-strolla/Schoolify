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

homepage = 'teacher.py'
result = 'error'
display = ''

base_page="""<body>

  <form action="login.py" class="form-signin">
    <img class="mb-4" src="{{ site.baseurl }}/docs/{{ site.docs_version }}/assets/brand/bootstrap-solid.svg" alt="" width="72" height="72">
    <h1 class="h3 mb-3 font-weight-normal"><center><img src="./assets/just_logo.png" width="125px" height="125px"></center></h1>
    <label for="inputEmail" class="sr-only">Email address</label>
    <input name="email" type="email" id="inputEmail" class="form-control" placeholder="Email address" required autofocus>
    <label for="inputPassword" class="sr-only">Password</label>
    <input name="password"type="password" id="inputPassword" class="form-control" placeholder="Password" required>
    <div class="checkbox mb-3">
      <label>
        <input type="checkbox" value="remember-me"> Remember me
      </label>
    </div>
    <button class="landing btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
  </form>

  <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
  <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
</body>"""

cookie = SimpleCookie()
http_cookie_header = environ.get('HTTP_COOKIE')

form_data = FieldStorage()
email = escape(form_data.getfirst('email', "").strip())
password = escape(form_data.getfirst('password', "").strip())

if email != '':
    connection = db.connect('cs1.ucc.ie', 'rjf1', 'ahf1Aeho', '2021_rjf1')
    cursor = connection.cursor(db.cursors.DictCursor)
    search_result = cursor.execute("""SELECT * FROM users WHERE email = %s AND password = %s""" , (email, password))
    fetched = cursor.fetchone()
    name= fetched['first_name'] + ' ' + fetched['last_name']
    account_type_check = cursor.execute("""SELECT account_type FROM users WHERE email = %s AND password = %s""" , (email, password))
    account_type = cursor.fetchone()
    account_type = account_type['account_type']
    account_type = str(account_type)

    #user found and password match, issue cookie and redirect to homepage
    if search_result == 1:
        cookie = SimpleCookie()
        sid = sha256(repr(time()).encode()).hexdigest()
        cookie['sid'] = sid
        session_store = open('sess_' + sid, writeback=True)
        session_store['authenticated'] = True
        session_store['username'] = email
        session_store['name'] = name
        session_store['account_type'] = account_type
        session_store.close()
        cursor.close()
        connection.close()
        print(cookie)
        if account_type == "1":
            print('Location: parent.py')
        elif account_type == "2":
            print('Location: teacher.py')
        else:
            print('Location: student.py')
    # incorrect username or password
    else:
        result="""<body>

          <form action="login.py" class="form-signin">
            <img class="mb-4" src="{{ site.baseurl }}/docs/{{ site.docs_version }}/assets/brand/bootstrap-solid.svg" alt="" width="72" height="72">
            <h1 class="h3 mb-3 font-weight-normal"><center><img src="./assets/just_logo.png" width="125px" height="125px"></center></h1>
            <p class="error-message"> Incorrect Username or Password </p>
            <p class="error-message"> Please try again </p>
            <label for="inputEmail" class="sr-only">Email address</label>
            <input name="email" type="email" id="inputEmail" class="form-control" placeholder="Email address" required autofocus>
            <label for="inputPassword" class="sr-only">Password</label>
            <input name="password"type="password" id="inputPassword" class="form-control" placeholder="Password" required>
            <div class="checkbox mb-3">
              <label>
                <input type="checkbox" value="remember-me"> Remember me
              </label>
            </div>
            <button class="landing btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
          </form>

          <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
          <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
          <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
        </body>"""

#if form is empty
else:
    #if cookie present
    if http_cookie_header:
        cookie.load(http_cookie_header)
        #if sid cookie
        if 'sid' in cookie:
            sid = cookie['sid'].value
            session_store = open('sess_' + sid, writeback=False)
            #if authenticated cookie redirect to homepage
            if session_store.get('authenticated'):
                if session_store['account_type'] == "1":
                    print('Location: parent.py')
                elif session_store['account_type'] == "2":
                    print('Location: teacher.py')
                else:
                    print('Location: student.py')
            #else unauthenticated cookie, display login/signup
            else:
                result=base_page
        #else no sid cookie present
        else:
            result=base_page
    #zero cookies present
    else:
        result=base_page




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
              <link rel="stylesheet" href="./css/style.css">
              <!--<link rel="icon" href="./assets/favicon.ico" type="image/x-icon">-->

              <title>Schoolify</title>
            </head>
            %s
        </html>""" % (result))
