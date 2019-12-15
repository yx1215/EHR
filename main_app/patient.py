from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

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
    all_doctors = db.execute("SELECT * FROM doctors").fetchall()
    provider = db.execute("SELECT * FROM take_care JOIN doctors ON take_care.doctor_id = doctors.id WHERE patient_id=?", (g.user['id'], )).fetchone()
    available_schedule = db.execute("SELECT * FROM doctors JOIN schedule s on doctors.id = s.doctor_id ORDER BY s.doctor_id").fetchall()
    my_past_schedule = db.execute("SELECT * FROM schedule "
                             "LEFT OUTER JOIN appointment a on schedule.doctor_id = a.doctor_id and schedule.start_time=a.start_time "
                             "LEFT OUTER JOIN doctors d on a.doctor_id = d.id WHERE a.patient_id=? AND a.status=?",
                             (g.user["id"], 'finished')).fetchall()

    my_upcoming_schedule = db.execute("SELECT * FROM schedule "
                             "LEFT OUTER JOIN appointment a on schedule.doctor_id = a.doctor_id and schedule.start_time=a.start_time "
                             "LEFT OUTER JOIN doctors d on a.doctor_id = d.id WHERE a.patient_id=? AND a.status<>?",
                             (g.user["id"], 'finished')).fetchall()

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
        his_d = {}
        his_d["start_time"] = r["start_time"]
        his_d["medical_his"] = r["medical_his"].split("\\n")
        medical_his_changed.append(his_d)

    comments_dic = {}
    for r in all_doctors:
        doctor_id = r['id']
        print(doctor_id)
        comments = db.execute("SELECT appointment.comments, p.first_name, p.last_name "
                              "FROM appointment JOIN patients p on appointment.patient_id = p.id "
                              "WHERE doctor_id=?", (doctor_id, )).fetchall()
        total = ""
        for c in comments:
            if c['comments'] is not None:
                total = total + c['last_name'] + " " + c['first_name'] + ":" + "\\n" + c["comments"] + "\\n"
        print(total)
        comments_dic[doctor_id] = total
    print(comments_dic)
    return render_template('./patient.html', my_provider=provider,  available_schedule=available_schedule,
                           my_provider_schedule=my_provider_schedule, medical_his=medical_his_changed,
                           need_appointment=need_appointment, my_past_schedule=my_past_schedule,
                           my_upcoming_schedule=my_upcoming_schedule, comments=comments_dic)


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


@patient_bp.route("/send_appointment", methods=('POST', 'GET'))
@login_required_patient
def send_appointment():
    doctor_id = request.args.get("doctor_id")
    patient_id = request.args.get("patient_id")
    start_time = request.args.get("start_time").split('T')
    start_time = start_time[0] + " " + start_time[1]
    duration = request.args.get("duration")

    db = get_db()
    error = None
    if db.execute("SELECT * FROM appointment WHERE doctor_id=? AND patient_id=? AND start_time=? AND duration=?",
                  (doctor_id, patient_id, start_time, duration)).fetchone() is not None:
        error = "There is a pending patient for the time slot, please wait for the doctor to accept."
    if error is None:
        db.execute('INSERT INTO appointment (doctor_id, patient_id, start_time, duration, location, status, medical_his, comments) '
                   'VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (doctor_id, patient_id, start_time, duration, 'not decided', 'pending', '', ''))
        db.commit()

        return redirect(url_for('patient.show_main'))
    flash(error)
    return redirect(url_for('patient.show_main'))


@patient_bp.route("/make_appointment_with_current_provider", methods=('POST', 'GET'))
@login_required_patient
def make_appointment_with_current_provider():
    doctor_id = request.args.get("doctor_id")
    patient_id = g.user['id']
    schedule_duration = request.args.get("schedule_duration")
    lst = schedule_duration.strip().split(",")
    start_time = lst[0].strip()
    duration = lst[1][:-3].strip()
    db = get_db()
    error = None
    if db.execute("SELECT * FROM appointment WHERE doctor_id=? AND patient_id=? AND start_time=? AND duration=?",
                  (doctor_id, patient_id, start_time, duration)).fetchone() is not None:
        error = "There is a pending patient for the time slot, please wait for the doctor to accept."
    if error is None:
        db.execute('INSERT INTO appointment (doctor_id, patient_id, start_time, duration, location, status, medical_his, comments) '
                   'VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (doctor_id, patient_id, start_time, duration, 'not decided', 'pending', '', ''))
        db.commit()

        return redirect(url_for('patient.show_main'))
    flash(error)
    return redirect(url_for('patient.show_main'))


@patient_bp.route('/comment', methods=("GET", "POST"))
@login_required_patient
def comment():
    appointment_id = request.args["appointment_id"]
    comments = request.args["comments"]
    db = get_db()
    db.execute('UPDATE appointment SET comments=? WHERE appointment_id=?',
               (comments, appointment_id))
    db.commit()
    return redirect(url_for('patient.show_main'))


@patient_bp.route('/cancel_appointment', methods=("GET", "POST"))
@login_required_patient
def cancel_appointment():
    appointment_id = request.args["appointment_id"]
    db = get_db()
    db.execute('DELETE FROM appointment WHERE appointment_id=?', (appointment_id, ))
    db.commit()
    return redirect(url_for('patient.show_main'))


@patient_bp.route('/message', methods=("GET", ))
@login_required_patient
def msg():
    return render_template("message.html")