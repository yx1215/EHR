from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash

from main_app.authentication import login_required
from main_app.database import get_db

patient_bp = Blueprint('patient', __name__, url_prefix="/patient")


@patient_bp.route("/patient_page/<int:id>", methods=('GET', 'POST'))
@login_required
def show_main(id):
    db = get_db()
    provider = db.execute("SELECT * FROM take_care JOIN doctors ON take_care.doctor_id = doctors.id WHERE patient_id=?", (id, )).fetchone()
    doctors = db.execute("SELECT * FROM doctors JOIN schedule s on doctors.id = s.doctor_id ORDER BY s.doctor_id").fetchall()
    return render_template('/patient.html', patient_id=id, my_provider=provider, all_doctors=doctors)


@patient_bp.route("/send_appointment", methods=('POST', ))
@login_required
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
    return redirect(url_for('patient.show_main', id=patient_id))
