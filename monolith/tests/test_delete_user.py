from monolith.database import User, Run, Objectives


def test_delete_user(client, db_instance):
    email = 'delete@test.com'
    password = 'password'

    client.post(
        '/create_user',
        data=dict(
            email=email,
            firstname='Jhon',
            lastname='Doe',
            password=password,
            age='22',
            weight='75',
            max_hr='150',
            rest_hr='60',
            vo2max='10'
        ),
        follow_redirects=True
    )

    user = db_instance.session.query(User).filter(User.email == email).first()
    user_id = user.get_id()

    runs_id = ['1', '2', '3']

    objective = Objectives()
    objective.distance = 1000
    objective.user = user

    for id in runs_id:
        run = Run()
        run.runner = user
        run.strava_id = id
        run.distance = 1500
        run.average_speed = 10
        run.elapsed_time = 200000
        db_instance.session.add(run)

    db_instance.session.add(objective)
    db_instance.session.commit()

    client.post(
        '/login',
        data=dict(
            email=email,
            password=password
        ),
        follow_redirects=True
    )

    client.post(
        '/delete_user',
        data=dict(
            password=password
        ),
        follow_redirects=True
    )

    user = db_instance.session.query(User).filter(User.email == email).first()
    assert user is None

    run = db_instance.session.query(Run).filter(Run.runner_id == user_id).first()
    assert run is None

    objective = db_instance.session.query(Objectives).filter(Objectives.user_id == user_id).first()
    assert objective is None
