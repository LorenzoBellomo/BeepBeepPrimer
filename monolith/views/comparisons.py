from flask import Blueprint, redirect, render_template, request
from monolith.database import db, User, Run, _delete_user
from monolith.auth import admin_required
from monolith.forms import UserForm, ComparisonsForm
from flask_login import current_user, logout_user

comparisons = Blueprint('comparisons', __name__)

@comparisons.route("/comparisons", methods=['POST'])
def post_comparisons():

    form = ComparisonsForm()

    runIds = form.data['runs']

    if runIds is None or len(runIds) <= 1:
        return redirect('/?comparisonError=Please select at least 2 runs.')

    if current_user is not None and hasattr(current_user, 'id'):
        runsId = list(map(int, runIds))
        runs = db.session.query(Run).filter(Run.runner_id == current_user.id, Run.id.in_(runIds))
    else:
        runs = []

    for r in runs:
        r.average_speed = "{:.2f}".format(r.average_speed * 3.6)
        r.elapsed_time = "{:.0f}".format(r.elapsed_time // 60) + "." + "{:.0f}".format(r.elapsed_time % 60)

    return render_template('comparisons.html', runs=runs)
