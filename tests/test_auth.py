import pytest
from flask import g, session
from main_app.database import get_db


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'first_name': 'a', 'last_name': 'a', 'password':'a','email':'123@nyu.edu','phone_number':'1234','gender': 'male'}
    )
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        assert get_db().execute(
            "select * from user where first_name = 'a'",
        ).fetchone() is not None


@pytest.mark.parametrize(('first_name', 'last_name','password', 'email','phone_number','gender','message'), (
    ('', 'a', 'a','123@nyu.edu','1234','male',b'first_name is required.'),
    ('a', '', 'a','123@nyu.edu','1234','male',b'last_name is required.'),
    ('a', 'a', '','123@nyu.edu','1234','male',b'password is required.'),
    ('a', 'a', 'a','','1234','male',b'email is required.'),
    ('a', 'a', 'a','123@nyu.edu','','male',b'phone_number is required.'),
    ('a', 'a', 'a','123@nyu.edu','1234','',b'gender is required.'),
    ('test', 'test', 'test', 'test', 'test', 'test', b'already registered')
))

def test_register_validate_input(client, first_name, last_name, password, email, phone_number, gender, message):
    response = client.post(
        '/auth/register',
        data={'first_name':first_name,
    'last_name':last_name,
    'password':password,
    'email':email,
    'phone_number':phone_number,
    'gender':gender
}
    )
    assert message in response.data


def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        assert session['user_id'] == 'b'
        assert g.user['first_name'] == 'test'


@pytest.mark.parametrize(('first_name', 'last_name','password', 'email','phone_number','gender','message'), (
    ('', 'a', 'a','123@nyu.edu','1234','male',b'first_name is required.'),
    ('a', '', 'a','123@nyu.edu','1234','male',b'last_name is required.'),
    ('a', 'a', '','123@nyu.edu','1234','male',b'password is required.'),
    ('a', 'a', 'a','','1234','male',b'email is required.'),
    ('a', 'a', 'a','123@nyu.edu','','male',b'phone_number is required.'),
    ('a', 'a', 'a','123@nyu.edu','1234','',b'gender is required.'),
    ('test', 'test', 'test', 'test', 'test', 'test', b'already registered')
))


def test_login_validate_input(auth, first_name, last_name, password, email, phone_number, gender, message):
    response = auth.login(
        '/auth/register',
        data={'first_name':first_name,
    'last_name':last_name,
    'password':password,
    'email':email,
    'phone_number':phone_number,
    'gender':gender
        }
    )
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session