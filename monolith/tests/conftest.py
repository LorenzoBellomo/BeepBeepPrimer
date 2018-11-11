import pytest
import os
from monolith.app import create_testing_app
from monolith.database import db
import subprocess


@pytest.fixture
def app():
    #subprocess.call(["./key.sh"])
    _app = create_testing_app()
    yield _app
    os.unlink('monolith/testdb.db')

@pytest.fixture
def db_instance(app):
    db.init_app(app)
    db.create_all(app=app)
    with app.app_context():
        yield db

@pytest.fixture
def client(app):
    client = app.test_client()

    yield client