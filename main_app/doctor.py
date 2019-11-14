from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash

from main_app.authentication import login_required
from main_app.database import get_db

doctor_bp = Blueprint('doctor', __name__, url_prefix="/doctor")


@doctor_bp.route("/doctor_page/<int:id>", methods=('GET', 'POST'))
@login_required
def show_main(id):
    db = get_db()
    pending_appointment = db.execute("SELECT * FROM appointment JOIN patients on patients.id=appointment.patient_id "
                                     "WHERE doctor_id=? and status=?",
                                     (id, 'pending')).fetchall()
    accepted_appointment = db.execute("SELECT * FROM appointment JOIN patients on patients.id=appointment.patient_id "
                                      "WHERE doctor_id=? and status=?",
                                     (id, 'accepted')).fetchall()
    return render_template('/doctor.html', doctor_id=id, pending=pending_appointment, accept=accepted_appointment)


@doctor_bp.route("/accept_appointment", methods=('POST', ))
@login_required
def accept_appointment():
    patient_id = request.args["patient_id"]
    doctor_id = request.args["doctor_id"]
    start_time = request.args["start_time"]
    db = get_db()
    db.execute("UPDATE schedule SET occupied=true WHERE doctor_id=? AND start_time=?", (doctor_id, start_time))
    db.execute("UPDATE appointment SET status = 'accepted' WHERE patient_id=? and doctor_id=? and start_time=?", (patient_id, doctor_id, start_time))
    db.execute("INSERT INTO take_care (doctor_id, patient_id) VALUES (?, ?)", (doctor_id, patient_id))
    db.commit()

    return redirect(url_for('doctor.show_main', id=doctor_id))


@doctor_bp.route("/set_schedule", methods=('POST', ))
@login_required
def set_schedule():
    doctor_id = request.args["doctor_id"]
    start_time = request.args["start_time"]
    duration = request.args["duration"]
    print(doctor_id, start_time, duration)
    db = get_db()
    db.execute("INSERT INTO schedule (doctor_id, start_time, duration, occupied) VALUES (?, ?, ?, ?)", (doctor_id, start_time, duration, False))
    db.commit()

    return redirect(url_for('doctor.show_main', id=doctor_id))

