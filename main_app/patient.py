from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash

from main_app.authentication import login_required
from main_app.database import get_db

patient_bp = Blueprint('patient', __name__, url_prefix="")


@patient_bp.route("/patient_page/<int:id>", methods=('GET', 'POST'))
@login_required
def show_main(id):
    return render_template('/patient.html')