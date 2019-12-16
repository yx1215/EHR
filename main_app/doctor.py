from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from main_app.authentication import login_required_doctor
from main_app.database import get_db

doctor_bp = Blueprint('doctor', __name__, url_prefix="/doctor")


@doctor_bp.route("/doctor_page", methods=('GET', 'POST'))
@login_required_doctor
def show_main():
    db = get_db()
    pending_appointment = db.execute("SELECT * FROM appointment JOIN patients on patients.id=appointment.patient_id "
                                     "WHERE doctor_id=? and status=?",
                                     (g.user["id"], 'pending')).fetchall()
    my_patient = db.execute("SELECT * FROM take_care JOIN patients on patients.id=take_care.patient_id "
                            "WHERE doctor_id=?",
                            (g.user["id"], )).fetchall()
    medical_his = db.execute("SELECT * FROM appointment WHERE doctor_id=? AND status<>'pending' ORDER BY start_time", (g.user["id"], )).fetchall()

    my_schedule = db.execute("SELECT schedule.start_time, schedule.duration, a.location, p.last_name, p.first_name, a.medical_his, a.appointment_id, a.status FROM schedule "
                             "LEFT OUTER JOIN appointment a on schedule.doctor_id = a.doctor_id and schedule.start_time=a.start_time "
                             "LEFT OUTER JOIN patients p on a.patient_id = p.id WHERE schedule.doctor_id=?",
                             (g.user["id"], )).fetchall()
    history_d = {}
    for r in medical_his:
        try:
            history_d[r["patient_id"]] = history_d[r["patient_id"]] + "\\n\\n" + str(r["start_time"]) + "\\n" + r["medical_his"]

        except:
            history_d[r["patient_id"]] = str(r["start_time"]) + "\\n" + r["medical_his"]

    return render_template('./doctor.html', pending=pending_appointment, my_patient=my_patient, my_schedule=my_schedule, medical_his_d=history_d)


@doctor_bp.route("/accept_appointment", methods=('POST', 'GET'))
@login_required_doctor
def accept_appointment():
    patient_id = request.args["patient_id"]
    doctor_id = request.args["doctor_id"]
    start_time = request.args["start_time"]
    db = get_db()
    db.execute("UPDATE schedule SET occupied=true WHERE doctor_id=? AND start_time=?", (doctor_id, start_time))
    db.execute("UPDATE appointment SET status = 'accepted' WHERE patient_id=? and doctor_id=? and start_time=?", (patient_id, doctor_id, start_time))
    if db.execute("SELECT * FROM take_care WHERE doctor_id=? AND patient_id=?", (doctor_id, patient_id)).fetchone() is None:
        db.execute("INSERT INTO take_care (doctor_id, patient_id) VALUES (?, ?)", (doctor_id, patient_id))
    db.commit()

    return redirect(url_for('doctor.show_main'))


@doctor_bp.route("/set_schedule", methods=('POST', 'GET'))
@login_required_doctor
def set_schedule():
    doctor_id = request.args["doctor_id"]
    start_time = request.args["start_time"].split("T")
    start_time = start_time[0] + " " + start_time[1] + ":00"
    duration = request.args["duration"]
    print(doctor_id, start_time, duration)
    db = get_db()
    db.execute("INSERT INTO schedule (doctor_id, start_time, duration, occupied) VALUES (?, ?, ?, ?)", (doctor_id, start_time, duration, False))
    db.commit()

    return redirect(url_for('doctor.show_main'))


@doctor_bp.route("/delete_schedule", methods=('POST', 'GET'))
@login_required_doctor
def delete_schedule():
    doctor_id = request.args["doctor_id"]
    start_time = request.args["start_time"]
    print(doctor_id, start_time)

    db = get_db()
    db.execute("DELETE FROM schedule WHERE start_time=? AND doctor_id=?", (start_time, doctor_id))
    db.commit()

    return redirect(url_for('doctor.show_main'))


@doctor_bp.route("/check_out", methods=('POST', 'GET'))
@login_required_doctor
def check_out():
    doctor_id = request.args["doctor_id"]
    patient_id = request.args["patient_id"]
    print(doctor_id, patient_id)
    db = get_db()
    db.execute("DELETE FROM take_care WHERE doctor_id=? AND patient_id=?", (doctor_id, patient_id))
    db.commit()

    return redirect(url_for('doctor.show_main'))


@doctor_bp.route("/write_medical_his", methods=('POST', 'GET'))
@login_required_doctor
def write_medical_his():
    appointment_id = request.args["appointment_id"]
    medical_his = request.args["medical_his"]
    print(appointment_id, medical_his)
    db = get_db()
    db.execute("UPDATE appointment SET medical_his=? WHERE appointment_id=?", (medical_his, appointment_id))
    db.commit()
    return redirect(url_for("doctor.show_main"))


@doctor_bp.route("/finish_appointment", methods=('GET', 'POST'))
@login_required_doctor
def finish_appointment():
    start_time = request.args['start_time']
    doctor_id = request.args['doctor_id']
    db = get_db()
    db.execute('UPDATE appointment SET status=? WHERE start_time=? AND doctor_id=?',
               ('finished', start_time, doctor_id))
    db.commit()
    return redirect(url_for('doctor.show_main'))


@doctor_bp.route('/message', methods=("GET", ))
@login_required_doctor
def msg():
    print("/message:", g.user)
    return render_template("message.html")
