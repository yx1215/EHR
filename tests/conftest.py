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

    def login(self, email='12345@nyu.edu',  password='xxx'):
        return self._client.post(
            '/auth/login',
            data={'login_type': 'patient', 'password': password, 'email': email,
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
