from monolith.database import User, Run, db, Challenge
from monolith.forms import ChallengeForm
from monolith.tests.utils import ensure_logged_in


def _copy_run(runs, index):
    r1 = Run()
    r1.runner = runs[index].runner
    r1.strava_id = runs[index].strava_id
    r1.name = runs[index].name
    r1.average_speed = runs[index].average_speed
    r1.elapsed_time = runs[index].elapsed_time
    r1.distance = runs[index].distance
    return r1


def test_challenge_run(client, db_instance):

    # simulate login
    user = ensure_logged_in(client, db_instance)

    # generate some runs
    runs = []
    for i in ['1', '2', '3', '4', '5']:
        # creating 5 incrementally better runs, except for the fourth one which is bad
        run = Run()

        run.runner = user
        run.strava_id = i
        run.name = "Run " + i
        if i != '4':
            run.average_speed = float(i)
            run.elapsed_time = float(i)*1000
            run.distance = 25 + float(i)
        else:
            run.average_speed = 0
            run.elapsed_time = 1
            run.distance = 1
        runs.append(run)

    # truncate runs table
    db_instance.session.query(Run).delete()
    db_instance.session.flush()
    db_instance.session.commit()

    r1 = _copy_run(runs, 0)
    r2 = _copy_run(runs, 1)

    db_instance.session.add(r1)
    db_instance.session.add(r2)

    db_instance.session.flush()
    db_instance.session.commit()

    # route back to index page
    res = client.post(
        '/challenge',
        data={
            'runs': ['1']
        },
        follow_redirects=True
    )

    challenged = db_instance.session.query(Challenge).filter(user.id == Run.runner_id).first()

    assert challenged
    assert challenged.run_id == 1

    r3 = _copy_run(runs, 2)
    r4 = _copy_run(runs, 3)
    r5 = _copy_run(runs, 4)

    db_instance.session.add(r3)
    db_instance.session.add(r4)
    db_instance.session.add(r5)

    db_instance.session.flush()
    db_instance.session.commit()

    toCompare = db_instance.session.query(Run).filter(user.id == Run.runner_id, Run.id > challenged.latest_run_id).all()

    assert len(toCompare) == 3

    better = 0
    worse = 0
    for run in toCompare:
        if run.average_speed > challenged.run.average_speed and run.distance > challenged.run.distance:
            better += 1
        else:
            worse += 1

    assert better == 2
    assert worse == 1
    assert better + worse == 3

    res = client.post(
        '/challenge',
        data={
            'runs': ['1']
        },
        follow_redirects=True
    )

    challenged = db_instance.session.query(Challenge).filter(user.id == Run.runner_id).first()

    assert not challenged
