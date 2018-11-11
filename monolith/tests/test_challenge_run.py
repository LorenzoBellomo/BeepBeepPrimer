from monolith.database import User, Run, db, Challenge
from monolith.forms import ChallengeForm
from monolith.tests.utils import ensure_logged_in


def test_challenge_run(client, db_instance):

    # simulate login
    user = ensure_logged_in(client, db_instance)

    # generate some runs
    runs = []
    for i in ['1', '2', '3', '4', '5']:
        #creating 5 incrementally better runs, except for the one with id 4 which is bad
        run = Run()

        run.runner = user
        run.strava_id = i
        run.name = "Run " + i
        if i != '4':
            run.average_speed = float(i)
            run.elapsed_time = float(i)*1000
            run.distance = 25
        else:
            run.average_speed = 0
            run.elapsed_time = 1
            run.distance = 1

        runs.append(run)

    #inserting only the first 2 to the database
    db_instance.session.add(runs[0])
    db_instance.session.add(runs[1])
    db_instance.session.commit()

    # route back to index page
    res = client.post(
        '/challenge',
        data={
            'runs': ['1']
        },
        follow_redirects=True
    )

    challenged = db.session.query(Challenge).filter(user.id == Run.runner_id).first()
    assert challenged
    assert challenged.run_id == 1
    db_instance.session.add(runs[2])
    db_instance.session.add(runs[3])
    db_instance.session.add(runs[4])

    db_instance.session.commit()

    toCompare = db_instance.session.query(Run).filter(current_user.id == Run.runner_id, Run.id > challenged.latest_run_id).all()
    assert len(toCompare) == 3
    for run in toCompare:
        better = 0
        worse = 0
        if run.average_speed > challenged.run.average_speed and run.distance > challenged.run.distance:
            better += 1
        else:
            worse += 1
            assert run.id == 4

    assert better == 2
    assert worse == 1

    res = client.post(
        '/challenge',
        data={
            'runs': ['1']
        },
        follow_redirects=True
    )

    challenged = db.session.query(Challenge).filter(user.id == Run.runner_id).first()
    assert not challenged


    
