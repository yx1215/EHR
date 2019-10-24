import pytest
from flask import g, session
from main_app.database import get_db


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register',
        data={'register_type': 'patient', 'last_name': 'a', 'first_name': 'a', 'password': 'a', 'repeat_password': 'a', 'email': '123@nyu.edu',
              'phone_number': '1234', 'gender': 'female', 'height': '160.0', 'weight': '45.5',
              'birthday': '1998-11-18', 'emergency_contacts': '12345'}
    )

    assert '/auth/login' in response.headers['Location']

    with app.app_context():
        assert get_db().execute(
            "select * from patients where email = '123@nyu.edu'",
        ).fetchone() is not None


@pytest.mark.parametrize(('last_name', 'first_name', 'password', 'repeat_password', 'email', 'phone_number', 'gender', 'height', 'weight',
                          'birthday', 'emergency_contacts', 'medical_his', 'message'), (
                                 ('a', '', 'a', 'a', '123@nyu.edu', '1234', 'male', '160.0', '45.5', '1998-11-18', '12345',
                                  '', b'first name is required.'),
                                 ('', 'a', 'a', 'a', '123@nyu.edu', '1234', 'male', '160.0', '45.5', '1998-11-18', '12345',
                                  '', b'last name is required.'),
                                 ('a', 'a', '', '', '123@nyu.edu', '1234', 'male', '160.0', '45.5', '1998-11-18', '12345',
                                  '', b'password is required.'),
                                 ('a', 'a', 'a', 'a', '', '1234', 'male', '160.0', '45.5', '1998-11-18', '12345', '',
                                  b'email is required.'),
                                 ('a', 'a', 'a', 'a', '123@nyu.edu', '', 'male', '160.0', '45.5', '1998-11-18', '12345', '',
                                  b'phone_number is required.'),
                                 ('a', 'a', 'a', 'a', '123@nyu.edu', '1234', '', '160.0', '45.5', '1998-11-18', '12345', '',
                                  b'gender is required.'),
                                 ('a', 'a', 'a', 'b', '123@nyu.edu', '1234', '', '160.0', '45.5', '1998-11-18', '12345',
                                  '',
                                  b'two passwords are not the same.'),
                                 ('b', 'b', 'a', 'a', '12345@nyu.edu', '1234', 'male', '160.0', '45.5', '1998-11-18', '12345',
                                  '', b'Email 12345@nyu.edu has already registered.')
                         ))
def test_register_validate_input(client, last_name, first_name, password, repeat_password, email, phone_number, gender, height, weight,
                                 birthday, emergency_contacts, medical_his, message):
    response = client.post(
        '/auth/register',
        data={'register_type': 'patient', 'last_name': last_name, 'first_name': first_name, 'password': password,
              'repeat_password': repeat_password, 'email': email, 'phone_number': phone_number, 'gender': gender,
              'height': height, 'weight': weight,
              'birthday': birthday, 'emergency_contacts': emergency_contacts, 'medical_his': medical_his}
    )
    print("RESPONSE DATA:", response.data)
    assert message in response.data


def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    print("here", response.headers)
    assert 'http://localhost/patient/patient_page' in response.headers['Location']

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['first_name'] == 'a'


@pytest.mark.parametrize(('email', 'password', 'message'), (
        ('1235@nyu.edu', 'xxx', b'Incorrect username.'),
        ('12345@nyu.edu', 'xxxx', b'Incorrect password.')
))
def test_login_validate_input(auth, email, password, message):
    response = auth.login(email, password)
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
