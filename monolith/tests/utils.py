from monolith.database import User

# Creates a new user


def ensure_logged_in(client, db_instance):

    user = db_instance.session.query(User).filter(
        User.email == 'example@test.com').first()

    if(user is None):
        client.post(
            '/create_user',
            data=dict(
                email='example@test.com',
                firstname='Jhon',
                lastname='Doe',
                password='password',
                age='22',
                weight='75',
                max_hr='150',
                rest_hr='60',
                vo2max='10'
            ),
            follow_redirects=True
        )

    # simulate login
    client.post(
        '/login',
        data=dict(
            email='example@test.com',
            password='password'
        ),
        follow_redirects=True
    )

    user = db_instance.session.query(User).filter(User.email == 'example@test.com').first()

    return user
