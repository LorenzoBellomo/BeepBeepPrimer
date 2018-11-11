BeepBeep Skeleton
==================

How to run the app
-------------------

For this application to work, you need to create a Strava API application
see https://strava.github.io/api/#access and https://www.strava.com/settings/api

Once you have an application, you will have a "Client Id" and "Client Secret".
You need to export them as environment variables::

    export STRAVA_CLIENT_ID=<ID>
    export STRAVA_CLIENT_SECRET=<SECRET>

It is a good idea to create a file (and add it to .gitignore) that contains both commands. You can 
then run it via::

    source <filename>.sh

As usual, to start the app run::

    $ pip install -r requirements.txt
    $ python setup.py develop

You can then run your application with::

    $ python monolith/app.py
    * Running on http://127.0.0.1:5000/

How to create a new user
------------------------

1. Connect to Strava with the new user's account
2. Browse http://127.0.0.1:5000/create_user and insert data.
3. Login by browsing http://127.0.0.1:5000/
4. Click on "Authorize Strava Access" -- this will perform an OAuth trip to Strava.

Once authorized, you will be able to see your last 10 runs.
But for this, we need to ask the Celery worker to fetch them.

How to run the Celery worker
----------------------------

Make sure you have a redis server running locally on port 6379 by running::

    $ redis-server
    $ redis-cli
    $ 127.0.0.1:6379> ping
        PONG

Then, open another shell and run::

    $ celery worker -A monolith.background

This will run a celery microservice that can fetch runs.
To invoke it, visit http://127.0.0.1:5000/fetch.

Once the runs are retrieved, you should see your last ten runs
on http://127.0.0.1:5000

How to avoid the first sql alchemy warning
------------------------------------------

- edit the file ```  /home/you_user_name/.local/lib/python3.6/site-packages/flask_sqlalchemy/__init__.py ```

- at line 788
        
        track_modifications = app.config.setdefault(
            'SQLALCHEMY_TRACK_MODIFICATIONS', None
        )
        
        
- change None with False



