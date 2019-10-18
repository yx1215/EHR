from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash

from main_app.authentication import login_required
from main_app.database import get_db

admin_bp = Blueprint('admin', __name__, url_prefix="/admin")


def get_doctor(id):
    db = get_db()
    doctor = db.execute('SELECT * FROM doctors WHERE id = ?', (id, ))

    if doctor is None:
        abort(404, 'Doctor id {} is invalid.'.format(id))

    return doctor


@admin_bp.route('/admin_page', methods=('GET', 'POST'))
@login_required
def show_main():

    return render_template('/administrator.html')


@admin_bp.route('/add_doctor', methods=('GET', 'POST'))
@login_required
def add_doctor():
    if request.method == 'POST':
        db = get_db()
        error = None
        print(request.form)
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        password = request.form["password"]
        repeat_password = request.form["repeat_password"]
        email = request.form["email"]
        phone_number = request.form["phone_number"]
        gender = request.form["gender"]
        field = request.form['doctor_field']
        introduction = request.form['introduction']
        date_of_birth = request.form['birthday']
        date_of_join = request.form['date_of_join']

        if not last_name or not first_name:
            error = "name is required."
        elif not password:
            error = "password is required."
        elif not repeat_password:
            error = "repeat_password is required."
        elif password != repeat_password:
            error = "password and repeat_password not matched"
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
        elif not repeat_password:
            error = "repeat_password is required."

        if error is None:
            db.execute(
                'INSERT INTO doctors '
                '(password, first_name, last_name, email, phone_number, gender, field, introduction, date_of_birth, date_of_join) VALUES'
                '(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (generate_password_hash(password), first_name, last_name, email, phone_number, gender, field, introduction, date_of_birth, date_of_join)
                )
            db.commit()
            flash("Successfully add a doctor.")
            return render_template('/administrator.html')

        flash(error)
        # template not written
    return render_template('/administrator.html')


@admin_bp.route('/admin_page')
def show_doctor():
    db = get_db()
    all_doctors = db.execute('SELECT * FROM doctors').fetchall()
    # template not written
    return render_template('', all_doctors=all_doctors)


@admin_bp.route('/<int:id>/delete_doctor', methods=("POST", ))
@login_required
def delete_doctor(id):
    get_doctor(id)
    db = get_db()
    db.execute('DELETE FROM doctors WHERE id = ?', (id, ))
    db.commit()
    return redirect(url_for('admin.show_doctor'))