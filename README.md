# Flask-mongo-user-api

A take home from Heka Global

## Set up

It's good practice to setup a virutla environment for this python project

in the root directory run:

```
python3 -m venv venv
. venv/bin/activate
```

to enter the venv.

install all dependencies by run:

```
python3 -m pip install -r requirements.txt
```

This project also depend on a mongodb server, set up a free tier cluster and add the uri into `.env`

## Start the server

run:

```
flask --app flaskr run
```
