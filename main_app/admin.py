from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash

from main_app.authentication import login_required
from main_app.database import get_db

admin_bp = Blueprint('admin', __name__, url_prefix="")


@admin_bp.route('/admin')
def show_doctor():
    db = get_db()
    all_doctors = db.execute('SELECT * FROM doctors').fetchall()
    # template not written
    return render_template('', all_doctors=all_doctors)


def get_doctor(id):
    db = get_db()
    doctor = db.execute('SELECT * FROM doctors WHERE id = ?', (id, ))

    if doctor is None:
        abort(404, 'Doctor id {} is invalid.'.format(id))

    return doctor


@admin_bp.route('/register_doctor', methods=('GET', 'POST'))
@login_required
def register_doctor():
    if request.method == 'POST':
        db = get_db()
        error = None
        name = request.form["name"]
        password = request.form["password"]
        email = request.form["email"]
        phone_number = request.form["phone_number"]
        gender = request.form["gender"]
        field = request.form['field']
        introduction = request.form['introduction']
        date_of_birth = request.form['birthday']
        date_of_join = request.form['date_of_join']

        if not name:
            error = "name is required."
        elif not password:
            error = "password is required."
        elif not email:
            error = "email is required."
        elif not phone_number:
            error = "phone_number is required."
        elif not gender:
            error = "gender is required."
        elif not field:
            error = "field is required."
        elif not date_of_birth:
            error = "birthday is required."
        elif not date_of_join:
            error = "date of join is required."

        if error is None:
            db.execute(
                'INSERT INTO doctors '
                '(password, name, email, phone_number, gender, field, introduction, date_of_birth, date_of_join) VALUES'
                '(?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (generate_password_hash(password), name, email, phone_number, gender, field, introduction, date_of_birth, date_of_join)
                )
            db.commit()
            return redirect(url_for('admin.register_doctor'))

        flash(error)
        # template not written
    return render_template('/doctor.html')


@admin_bp.route('/<int:id>/delete_doctor', methods=("POST", ))
@login_required
def delete_doctor(id):
    get_doctor(id)
    db = get_db()
    db.execute('DELETE FROM doctors WHERE id = ?', (id, ))
    db.commit()
    return redirect(url_for('admin.show_doctor'))