import os
from flask import Flask
from monolith.database import db, User
from monolith.views import blueprints
from monolith.auth import login_manager


def create_app():
    app = Flask(__name__)
    app.config['WTF_CSRF_SECRET_KEY'] = 'ec35ae128aa97f834ab848ecf823340875ddf483e9a535440cf68e05b3b38865'
    app.config['SECRET_KEY'] = '58c8f1ffb80e7d48d936cb8a485504498fc6c5dcfce18e3de6dcd3b851ff0540'
    app.config['STRAVA_CLIENT_ID'] = os.environ['STRAVA_CLIENT_ID']
    app.config['STRAVA_CLIENT_SECRET'] = os.environ['STRAVA_CLIENT_SECRET']
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beepbeep.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    db.init_app(app)
    login_manager.init_app(app)
    db.create_all(app=app)

    # create a first admin user
    with app.app_context():
        q = db.session.query(User).filter(User.email == 'example@example.com')
        user = q.first()
        if user is None:
            example = User()
            example.email = 'example@example.com'
            example.is_admin = True
            example.set_password('admin')
            db.session.add(example)
            db.session.commit()
    return app

# used to create an app for testing
def create_testing_app():
    app = Flask(__name__)
    app.config['WTF_CSRF_SECRET_KEY'] = 'ec35ae128aa97f834ab848ecf823340875ddf483e9a535440cf68e05b3b38865'
    app.config['SECRET_KEY'] = '58c8f1ffb80e7d48d936cb8a485504498fc6c5dcfce18e3de6dcd3b851ff0540'
    app.config['STRAVA_CLIENT_ID'] = '00000'
    app.config['STRAVA_CLIENT_SECRET'] = '00000'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testdb.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_ENABLED'] = False # to mock rest services
    app.config['TESTING'] = True
    
    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    db.init_app(app)
    login_manager.init_app(app)
    db.create_all(app=app)

        # create a first admin user
    with app.app_context():
        q = db.session.query(User).filter(User.email == 'example@example.com')
        user = q.first()
        if user is None:
            example = User()
            example.email = 'example@example.com'
            example.is_admin = True
            example.set_password('admin')
            db.session.add(example)
            db.session.commit()
    return app

    return app

if __name__ == '__main__':
    app = create_app()
    # app.run(debug=True)
    app.run()
