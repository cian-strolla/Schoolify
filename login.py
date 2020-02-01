#!C:/Users/cians/AppData/Local/Programs/Python/Python38/python.exe

from cgitb import enable
enable()

from cgi import FieldStorage, escape
import pymysql as db
from hashlib import sha256
from time import time
from shelve import open
from http.cookies import SimpleCookie
from os import environ

homepage = 'homepage.py'
result = 'error'
display = ''

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
        if session_store.get('authenticated'):
            print('Location: homepage.py')
        #else unauthenticated cookie, display login/signup
        else:
            result = """<body>
                <header>
                    <h1>Homepage</h1>
                    <h1>Login or Sign Up Below</h1>
                </header>
                <main>
                    <div id ="logindiv">
                        <button id="loginbutton">Login</button>
                        <p id = o_p_o style="color:red">
                            Incorrect details entered. Please check credentials and try again:
                        </p>
                        <form action="login.py" method="post" id="login">
                            <label for="username">Enter Username: </label>
                            <input type="text" name="username" id="username" />
                            <label for="password">Enter Password: </label>
                            <input type="password" name="password" id="password" />
                            <input type="submit" value="Login" id = "submitbutton"/>
                        </form>
                        <div id = "closelog">
                            <button id="closelogin">Close Login</button>
                        </div>
                        <section id="accountcreationsidetext">
                            <ul>
                                <li>Create Account</li>
                                <li>Chat with Friends</li>
                                <li>Have Fun</li>
                            </ul>
                        </section>
                    </div>
                    <div id=accountcreation>
                        <button id="createaccountbutton">Create an Account</button>
                        <section id="loginsidetext">
                            <ul>
                                <li>Welcome Back</li>
                                <li>Going to your Homepage</li>
                            </ul>
                        </section>
                        <p id = o_p_p>
                            Create your Account:
                        </p>
                        <form action="register.py" method="post" id="createaccount">
                            <label for="firstname">Enter Details: </label>
                            <input type="text" name="firstname" id="firstname" placeholder="Firstname"/>
                            <input type="text" name="lastname" id="lastname" placeholder="Lastname" />
                            <label for ="email">Username must not contain spaces</label>
                            <input type="text" name="email" id="email" placeholder="Username" />
                            <input type="password" name="password" id="newpassword" placeholder="New password" />
                            <label for="birthday">Birthday: </label>
                            <input type="date" name="birthday" id="birthday" />
                            <label for="gender" id = "genderlabel">Gender: </label>
                            <label for="male">Male</label>
                            <input type="radio" name="gender" value="Male" id="male" />
                            <label for="female">Female</label>
                            <input type="radio" name="gender" value="Female" id="female" />
                            <input type="submit" value="Create Account"  id = "submitbutton"/>
                        </form>
                        <div id = "closeca">
                            <button id="closecreateaccount">Close Create an Account</button>
                        </div>
                    </div>

                </main>
            </body>"""

    #else no sid cookie present
    else:
        form_data = FieldStorage()
        email = escape(form_data.getfirst('username', "").strip())
        password = escape(form_data.getfirst('password', "").strip())

        sha256_password = sha256(password.encode()).hexdigest()
        if email != '':
            connection = db.connect('localhost', 'root', '', 'social_network')
            cursor = connection.cursor(db.cursors.DictCursor)
            search_result = cursor.execute("""SELECT * FROM users WHERE email = %s AND passwrd = %s""" , (email, sha256_password))

            #user found and password match, issue cookie and redirect to homepage
            if search_result == 1:
                cookie = SimpleCookie()
                sid = sha256(repr(time()).encode()).hexdigest()
                cookie['sid'] = sid
                session_store = open('sess_' + sid, writeback=True)
                session_store['authenticated'] = True
                session_store['username'] = email
                session_store.close()
                cursor.close()
                connection.close()
                print(cookie)
                print('Location: homepage.py')

            #else user not found, redisplay login
            else:
                result = """<body>
                <header>
                    <h1>Homepage</h1>
                    <h1>Login or Sign Up Below</h1>
                </header>
                <main>
                    <div id ="logindiv">
                        <button id="loginbutton">Login</button>
                        <p id = o_p_o style="color:red">
                            Incorrect details entered. Please check credentials and try again:
                        </p>
                        <form action="login.py" method="post" id="login">
                            <label for="username">Enter Username: </label>
                            <input type="text" name="username" id="username" />
                            <label for="password">Enter Password: </label>
                            <input type="password" name="password" id="password" />
                            <input type="submit" value="Login" id = "submitbutton"/>
                        </form>
                        <div id = "closelog">
                            <button id="closelogin">Close Login</button>
                        </div>
                        <section id="accountcreationsidetext">
                            <ul>
                                <li>Create Account</li>
                                <li>Chat with Friends</li>
                                <li>Have Fun</li>
                            </ul>
                        </section>
                    </div>
                    <div id=accountcreation>
                        <button id="createaccountbutton">Create an Account</button>
                        <section id="loginsidetext">
                            <ul>
                                <li>Welcome Back</li>
                                <li>Going to your Homepage</li>
                            </ul>
                        </section>
                        <p id = o_p_p>
                            Create your Account:
                        </p>
                        <form action="register.py" method="post" id="createaccount">
                            <label for="firstname">Enter Details: </label>
                            <input type="text" name="firstname" id="firstname" placeholder="Firstname"/>
                            <input type="text" name="lastname" id="lastname" placeholder="Lastname" />
                            <label for ="email">Username must not contain spaces</label>
                            <input type="text" name="email" id="email" placeholder="Username" />
                            <input type="password" name="password" id="newpassword" placeholder="New password" />
                            <label for="birthday">Birthday: </label>
                            <input type="date" name="birthday" id="birthday" />
                            <label for="gender" id = "genderlabel">Gender: </label>
                            <label for="male">Male</label>
                            <input type="radio" name="gender" value="Male" id="male" />
                            <label for="female">Female</label>
                            <input type="radio" name="gender" value="Female" id="female" />
                            <input type="submit" value="Create Account"  id = "submitbutton"/>
                        </form>
                        <div id = "closeca">
                            <button id="closecreateaccount">Close Create an Account</button>
                        </div>
                    </div>

                </main>
            </body>"""
            connection.commit()
            cursor.close()
            connection.close()

        #no credentials given, display original login page
        else:
            result = """<body>
                <header>
                    <h1>Homepage</h1>
                    <h1>Login or Sign Up Below</h1>
                </header>
                <main>
                    <div id ="logindiv">
                        <button id="loginbutton">Login</button>
                        <form action="login.py" method="post" id="login">
                            <label for="username">Enter Username: </label>
                            <input type="text" name="username" id="username" />
                            <label for="password">Enter Password: </label>
                            <input type="password" name="password" id="password" />
                            <input type="submit" value="Login" id = "submitbutton"/>
                        </form>
                        <div id = "closelog">
                            <button id="closelogin">Close Login</button>
                        </div>
                        <section id="accountcreationsidetext">
                            <ul>
                                <li>Create Account</li>
                                <li>Chat with Friends</li>
                                <li>Have Fun</li>
                            </ul>
                        </section>
                    </div>
                    <div id=accountcreation>
                        <button id="createaccountbutton">Create an Account</button>
                        <section id="loginsidetext">
                            <ul>
                                <li>Welcome Back</li>
                                <li>Going to your Homepage</li>
                            </ul>
                        </section>
                        <p id = o_p_p>
                            Create your Account:
                        </p>
                        <form action="register.py" method="post" id="createaccount">
                            <label for="firstname">Enter Details: </label>
                            <input type="text" name="firstname" id="firstname" placeholder="Firstname"/>
                            <input type="text" name="lastname" id="lastname" placeholder="Lastname" />
                            <label for ="email">Username must not contain spaces</label>
                            <input type="text" name="email" id="email" placeholder="Username" />
                            <input type="password" name="password" id="newpassword" placeholder="New password" />
                            <label for="birthday">Birthday: </label>
                            <input type="date" name="birthday" id="birthday" />
                            <label for="gender" id = "genderlabel">Gender: </label>
                            <label for="male">Male</label>
                            <input type="radio" name="gender" value="Male" id="male" />
                            <label for="female">Female</label>
                            <input type="radio" name="gender" value="Female" id="female" />
                            <input type="submit" value="Create Account"  id = "submitbutton"/>
                        </form>
                        <div id = "closeca">
                            <button id="closecreateaccount">Close Create an Account</button>
                        </div>
                    </div>

                </main>
            </body>"""

#zero cookies present
else:
    form_data = FieldStorage()
    email = escape(form_data.getfirst('username', "").strip())
    password = escape(form_data.getfirst('password', "").strip())

    sha256_password = sha256(password.encode()).hexdigest()
    if email != '':

        connection = db.connect('localhost', 'root', '', 'social_network')
        cursor = connection.cursor(db.cursors.DictCursor)
        cursor.execute("""SELECT * FROM users WHERE email = %s AND passwrd = %s""" , (email, sha256_password))


        if cursor.rowcount == 1:
            cookie = SimpleCookie()
            sid = sha256(repr(time()).encode()).hexdigest()
            cookie['sid'] = sid
            session_store = open('sess_' + sid, writeback=True)
            session_store['authenticated'] = True
            session_store['username'] = email
            session_store.close()
            print(cookie)
            print('Location: homepage.py')
            cursor.close()
            connection.close()
        else:
            result = """<body>
                    <header>
                        <h1>Homepage</h1>
                        <h1>Login or Sign Up Below</h1>
                    </header>
                    <main>
                        <div id ="logindiv">
                            <button id="loginbutton">Login</button>
                            <p id = o_p_o style="color:red">
                                Incorrect details entered. Please check credentials and try again:
                            </p>
                            <form action="login.py" method="post" id="login">
                                <label for="username">Enter Username: </label>
                                <input type="text" name="username" id="username" />
                                <label for="password">Enter Password: </label>
                                <input type="password" name="password" id="password" />
                                <input type="submit" value="Login" id = "submitbutton"/>
                            </form>
                            <div id = "closelog">
                                <button id="closelogin">Close Login</button>
                            </div>
                            <section id="accountcreationsidetext">
                                <ul>
                                    <li>Create Account</li>
                                    <li>Chat with Friends</li>
                                    <li>Have Fun</li>
                                </ul>
                            </section>
                        </div>
                        <div id=accountcreation>
                            <button id="createaccountbutton">Create an Account</button>
                            <section id="loginsidetext">
                                <ul>
                                    <li>Welcome Back</li>
                                    <li>Going to your homepage</li>
                                </ul>
                            </section>
                            <p id = o_p_p>
                                Create your Account:
                            </p>
                            <form action="register.py" method="post" id="createaccount">
                                <label for="firstname">Enter Details: </label>
                                <input type="text" name="firstname" id="firstname" placeholder="Firstname"/>
                                <input type="text" name="lastname" id="lastname" placeholder="Lastname" />
                                <label for ="email">Username must not contain spaces</label>
                                <input type="text" name="email" id="email" placeholder="Username" />
                                <input type="password" name="password" id="newpassword" placeholder="New password" />
                                <label for="birthday">Birthday: </label>
                                <input type="date" name="birthday" id="birthday" />
                                <label for="gender" id = "genderlabel">Gender: </label>
                                <label for="male">Male</label>
                                <input type="radio" name="gender" value="Male" id="male" />
                                <label for="female">Female</label>
                                <input type="radio" name="gender" value="Female" id="female" />
                                <input type="submit" value="Create Account"  id = "submitbutton"/>
                            </form>
                            <div id = "closeca">
                                <button id="closecreateaccount">Close Create an Account</button>
                            </div>
                        </div>

                    </main>
                </body>"""
    else:
       result = """<body>
                    <header>
                        <h1>Homepage</h1>
                        <h1>Login or Sign Up Below</h1>
                    </header>
                    <main>
                        <div id ="logindiv">
                            <button id="loginbutton">Login</button>
                            <p id = o_p_o style="color:red">
                                Incorrect details entered. Please check credentials and try again:
                            </p>
                            <form action="login.py" method="post" id="login">
                                <label for="username">Enter Username: </label>
                                <input type="text" name="username" id="username" />
                                <label for="password">Enter Password: </label>
                                <input type="password" name="password" id="password" />
                                <input type="submit" value="Login" id = "submitbutton"/>
                            </form>
                            <div id = "closelog">
                                <button id="closelogin">Close Login</button>
                            </div>
                            <section id="accountcreationsidetext">
                                <ul>
                                    <li>Create Account</li>
                                    <li>Chat with Friends</li>
                                    <li>Have Fun</li>
                                </ul>
                            </section>
                        </div>
                        <div id=accountcreation>
                            <button id="createaccountbutton">Create an Account</button>
                            <section id="loginsidetext">
                                <ul>
                                    <li>Welcome Back</li>
                                    <li>Going to your homepage</li>
                                </ul>
                            </section>
                            <p id = o_p_p>
                                Create your Account:
                            </p>
                            <form action="register.py" method="post" id="createaccount">
                                <label for="firstname">Enter Details: </label>
                                <input type="text" name="firstname" id="firstname" placeholder="Firstname"/>
                                <input type="text" name="lastname" id="lastname" placeholder="Lastname" />
                                <label for ="email">Username must not contain spaces</label>
                                <input type="text" name="email" id="email" placeholder="Username" />
                                <input type="password" name="password" id="newpassword" placeholder="New password" />
                                <label for="birthday">Birthday: </label>
                                <input type="date" name="birthday" id="birthday" />
                                <label for="gender" id = "genderlabel">Gender: </label>
                                <label for="male">Male</label>
                                <input type="radio" name="gender" value="Male" id="male" />
                                <label for="female">Female</label>
                                <input type="radio" name="gender" value="Female" id="female" />
                                <input type="submit" value="Create Account"  id = "submitbutton"/>
                            </form>
                            <div id = "closeca">
                                <button id="closecreateaccount">Close Create an Account</button>
                            </div>
                        </div>

                    </main>
                </body>"""


print('Content-Type: text/html')
print()

print("""
    <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="utf-8" />
                <title>Login</title>
                <link rel="stylesheet" href="index.css" />
                <link href="https://fonts.googleapis.com/css?family=Fira+Sans" rel="stylesheet">
                <script src="login1.js"></script>
                <meta name="viewport" content="initial-scale=1.0, width=device-width" />
            </head>
            %s
        </html>""" % (result))
