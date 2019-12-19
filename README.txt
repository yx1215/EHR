To execute our app, environment has to be set in terminal.
Make sure that you are in
    ./EHR
directory

Then run the following instruction in the terminal:
    export FLASK_ENV=development
    export FLASK_APP=main_app

And then execute:

    flask run

to run the main system.

And then go to

    ./message_system

directory
and run

    node app.js

to run the backend for message system.

Then go to Chrome and go to http://127.0.0.1/auth/login to begin.