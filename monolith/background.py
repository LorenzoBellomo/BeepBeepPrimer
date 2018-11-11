#Use for send email
import smtplib
import datetime
import email.message
from celery.schedules import crontab

from celery import Celery
from stravalib import Client
from monolith.database import db, User, Run

import os
CELERY_CONFIG = {
    'CELERY_BROKER_URL':
     'redis://{}'.format(os.environ.get('REDIS_URL', 'localhost:6379')),
  'CELERY_TASK_SERIALIZER': 'json',
}

celery = Celery(__name__, broker=CELERY_CONFIG['CELERY_BROKER_URL'])
celery.conf.update(CELERY_CONFIG)

_APP = None
_current_module = __import__(__name__)


@celery.task
def fetch_all_runs():
    global _APP
    # lazy init
    if _APP is None:
        from monolith.app import create_app
        app = create_app()
        db.init_app(app)
    else:
        app = _APP

    runs_fetched = {}

    with app.app_context():
        q = db.session.query(User)
        for user in q:
            if user.strava_token is None:
                continue
            print('Fetching Strava for %s' % user.email)
            runs_fetched[user.id] = fetch_runs(user)

    return runs_fetched

def add_to_module(f):
    setattr(_current_module, 'tasks_{}__'.format(f.__name__), f)
    return f

def get_from_module(f):
    return getattr(_current_module, 'tasks_{}__'.format(f))

@add_to_module
@celery.task
def send_email(reciver, deltatime):
    global _APP
    # lazy init
    if _APP is None:
        from monolith.app import create_app
        app = create_app()
        db.init_app(app)
    else:
        app = _APP

    now = datetime.datetime.now()
    email_content = """
        <html>
            <body>
                cose a caso dette in mezzo
            </body>
        </html>
        """

    # make email
    msg = email.message.Message()
    msg['From'] = "beepbeep.report@gmail.com"
    msg['To'] = reciver #"r.santo1@studenti.unipi.it"

    msg['Subject'] = deltatime + "BeepBeep Report of " + str(now.day) + "-" + str(now.month)
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(email_content)

    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(msg['From'], "Password1\"")
    server.sendmail(msg['From'], [msg['To']], msg.as_string())
    server.quit()

    print("successfully sent email to %s: "+msg['To'])

def activity2run(user, activity):
    """Used by fetch_runs to convert a strava run into a DB entry.
    """
    run = Run()
    run.runner = user
    run.strava_id = activity.id
    run.name = activity.name
    run.distance = activity.distance
    run.elapsed_time = activity.elapsed_time.total_seconds()
    run.average_speed = activity.average_speed
    run.average_heartrate = activity.average_heartrate
    run.total_elevation_gain = activity.total_elevation_gain
    run.start_date = activity.start_date
    return run

def fetch_runs(user):
    client = Client(access_token=user.strava_token)
    runs = 0

    for activity in client.get_activities(limit=10):# TODO: delete limit
        if activity.type != 'Run':
            continue
        q = db.session.query(Run).filter(Run.strava_id == activity.id)
        run = q.first()

        if run is None:
            db.session.add(activity2run(user, activity))
            runs += 1

    db.session.commit()
    return runs

def add_task_report(email):
    job = {
        'task': 'send_email',               # Name of a predefined function
        'schedule': 30, # crontab schedule
        'args': [email, "Tasks"],
        'kwargs': {},
    }
    if not isinstance(job, dict) and 'task' in jobs:
        print("Job {} is ill-formed".format(job))
        return False
    celery.add_periodic_task(
        30,
        get_from_module(job['task']).s(
            *job.get('args', []),
            **job.get('kwargs', {})
        ),
        name = job.get('name'),
        expires = job.get('expires')
    )
    print("Added periodic job: %s", job)

# add_task_report("r.santo1@studenti.unipi.it")
