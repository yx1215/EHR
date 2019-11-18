from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash

from main_app.authentication import login_required_patient
from main_app.database import get_db

patient_bp = Blueprint('patient', __name__, url_prefix="/patient")


@patient_bp.route("/patient_page", methods=('GET', 'POST'))
@login_required_patient
def show_main():
    db = get_db()
    provider = db.execute("SELECT * FROM take_care JOIN doctors ON take_care.doctor_id = doctors.id WHERE patient_id=?", (g.user['id'], )).fetchone()
    doctors = db.execute("SELECT * FROM doctors JOIN schedule s on doctors.id = s.doctor_id ORDER BY s.doctor_id").fetchall()
    if provider is not None:
        my_provider_schedule = db.execute("SELECT * FROM schedule WHERE doctor_id=?", (provider["id"], ))
    else:
        my_provider_schedule = None
    return render_template('/patient.html', my_provider=provider, all_doctors=doctors, my_provider_schedule=my_provider_schedule)


@patient_bp.route("/send_appointment", methods=('POST', ))
@login_required_patient
def send_appointment():
    doctor_id = request.args.get("doctor_id")
    patient_id = request.args.get("patient_id")
    start_time = request.args.get("start_time")
    duration = request.args.get("duration")
    print(request.args)
    db = get_db()
    db.execute('INSERT INTO appointment (doctor_id, patient_id, start_time, duration, location, status) '
               'VALUES (?, ?, ?, ?, ?, ?)', (doctor_id, patient_id, start_time, duration, 'not decided', 'pending'))
    db.commit()
    return redirect(url_for('patient.show_main'))


@patient_bp.route("/make_appointment_with_current_provider", methods=('POST', ))
@login_required_patient
def make_appointment_with_current_provider():
    doctor_id = request.args.get("doctor_id")
    patient_id = g.user['id']
    schedule_duration = request.args.get("schedule_duration")
    lst = schedule_duration.strip().split(",")
    start_time = lst[0].strip()
    duration = lst[1][:-3].strip()
    print(doctor_id, start_time, duration)
    db = get_db()
    db.execute('INSERT INTO appointment (doctor_id, patient_id, start_time, duration, location, status) '
               'VALUES (?, ?, ?, ?, ?, ?)', (doctor_id, patient_id, start_time, duration, 'not decided', 'pending'))
    db.commit()

    return redirect(url_for('patient.show_main'))
