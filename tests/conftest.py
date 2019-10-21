import tempfile
import os

import pytest
from main_app import create_app

from main_app.database import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'testdata.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()

class AuthActions(object):
    def __init__(self, client):
        self._client = client
    def login(self, first_name = 'a', last_name = 'a', password = 'a', email='123@nyu.edu', phone_number='1234', gender='male'):
        return self._client.post(
            '/auth/login',
            data={'first_name':first_name,
    'last_name':last_name,
    'password':password,
    'email':email,
    'phone_number':phone_number,
    'gender':gender
}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
