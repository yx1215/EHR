import os
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'main_app.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/welcome')
    def welcome():
        return "Welcome to our EHR system."

    from . import database
    database.init_app(app)

    from . import authentication
    app.register_blueprint(authentication.auth_bp)

    from . import admin
    app.register_blueprint(admin.admin_bp)

    from . import patient
    app.register_blueprint(patient.patient_bp)

    from . import doctor
    app.register_blueprint(doctor.doctor_bp)

    return app
