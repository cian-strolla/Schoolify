# Schoolify

Schoolify is an online school administration system for students, parents and teachers

Running the Application:

```sh
$ cd src

$ python mywebserver.py
```

this should provide a message `Serving HTTP on 0.0.0.0 port 8000 ...`
go to localhost:8000/cgi-bin/teacher.py (or /index.py etc)


to visit the site running on the CS servers go to `cs1.ucc.ie/~ram6/cgi-bin/Schoolify/src/login.py` etc..

## Fixes to certain issues

If this error: `DevTools failed to parse SourceMap: chrome-extension://cfhdojbkjhnklbpkdaibdccddilifddb/include.preload.js.map`
appears in the chrome dev tools, try disabling "Enable Javascript source maps" in the devTools settings.

Error with KeyObject in shelve.py, try deleting cookies.
