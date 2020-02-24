# Schoolify

Schoolify is an online school administration system for students, parents and teachers

Running the Application:

Clone the repo inside the /public_html/cgi-bin of your private cs1 server. Change all
permissions using `chmod -R 755 Schoolify`. Visit website by searching for `cs1.ucc.ie/~{YOUR USERNAME HERE}/cgi-bin/Schoolify/src/login.py`.

To visit a working example on the CS servers go to `cs1.ucc.ie/~ram6/cgi-bin/Schoolify/src/login.py` etc..

## Fixes to certain issues

If this error: `DevTools failed to parse SourceMap: chrome-extension://cfhdojbkjhnklbpkdaibdccddilifddb/include.preload.js.map`
appears in the chrome dev tools, try disabling "Enable Javascript source maps" in the devTools settings.

Error with KeyObject in shelve.py, try deleting cookies.

Disable any add-ons that interfere with form input, i.e. Lastpass for me personally.
