from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash

from main_app.authentication import login_required_patient
from main_app.database import get_db
from datetime import datetime
from dateutil.relativedelta import relativedelta
patient_bp = Blueprint('patient', __name__, url_prefix="/patient")


@patient_bp.route("/patient_page", methods=('GET', 'POST'))
@login_required_patient
def show_main():
    time = str(datetime.now() - relativedelta(days=30))
    db = get_db()
    provider = db.execute("SELECT * FROM take_care JOIN doctors ON take_care.doctor_id = doctors.id WHERE patient_id=?", (g.user['id'], )).fetchone()
    doctors = db.execute("SELECT * FROM doctors JOIN schedule s on doctors.id = s.doctor_id ORDER BY s.doctor_id").fetchall()

    if provider is not None:
        my_provider_schedule = db.execute("SELECT * FROM schedule WHERE doctor_id=?", (provider["id"], ))
    else:
        my_provider_schedule = None
    medical_his = db.execute("SELECT start_time, medical_his FROM appointment WHERE patient_id=? ORDER BY start_time", (g.user['id'], )).fetchall()
    medical_his_changed = []
    check_appointment = db.execute("SELECT * FROM appointment WHERE start_time>? AND patient_id=?", (time, g.user['id'])).fetchone()

    if check_appointment is None:
        need_appointment = True
    else:
        need_appointment = False

    for r in medical_his:
        new_d = {}
        new_d["start_time"] = r["start_time"]
        new_d["medical_his"] = r["medical_his"].split("\\n")
        print(new_d)
        medical_his_changed.append(new_d)
    return render_template('./patient.html', my_provider=provider, all_doctors=doctors,
                           my_provider_schedule=my_provider_schedule, medical_his=medical_his_changed,
                           need_appointment=need_appointment)


@patient_bp.route('/edit_info', methods=('POST', ))
@login_required_patient
def edit_info():
    weight = request.form["weight"]
    height = request.form["height"]
    emergency_contacts = request.form["emergency_contacts"]
    db = get_db()
    db.execute('UPDATE patients SET weight=?, height=?, emergency_contacts=? WHERE id=?',
               (weight, height, emergency_contacts, g.user["id"]))
    db.commit()
    return redirect(url_for('patient.show_main'))


@patient_bp.route("/send_appointment", methods=('POST', ))
@login_required_patient
def send_appointment():
    doctor_id = request.args.get("doctor_id")
    patient_id = request.args.get("patient_id")
    start_time = request.args.get("start_time").split('T')
    start_time = start_time[0] + " " + start_time[1]
    duration = request.args.get("duration")
    print(start_time)
    db = get_db()
    db.execute('INSERT INTO appointment (doctor_id, patient_id, start_time, duration, location, status, medical_his) '
               'VALUES (?, ?, ?, ?, ?, ?, ?)', (doctor_id, patient_id, start_time, duration, 'not decided', 'pending', ''))
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
    db.execute('INSERT INTO appointment (doctor_id, patient_id, start_time, duration, location, status, medical_his) '
               'VALUES (?, ?, ?, ?, ?, ?, ?)', (doctor_id, patient_id, start_time, duration, 'not decided', 'pending', ''))
    db.commit()

    return redirect(url_for('patient.show_main'))


@patient_bp.route('/message', methods=("GET", ))
@login_required_patient
def msg():
    return render_template("message.html")