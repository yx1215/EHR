from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash

from main_app.authentication import login_required
from main_app.database import get_db

doctor_bp = Blueprint('doctor', __name__, url_prefix="")


@doctor_bp.route("/doctor_page", methods=('GET', 'POST'))
@login_required
def show_main():
    return render_template('/doctor.html')
