from flask import Blueprint, render_template
from monolith.database import db, Run
from monolith.auth import current_user

runs = Blueprint('runs', __name__)


@runs.route('/runs/<int:run_id>')
def _runs(run_id):
    if current_user is not None and hasattr(current_user, 'id'):
        runs = db.session.query(Run).filter(Run.runner_id == current_user.id, Run.id == run_id).first()
        prev_run = db.session.query(Run).filter(Run.runner_id == current_user.id, Run.id < run_id).order_by(Run.id.desc()).first()
    else:
        runs = None
        prev_run = None;
    return render_template("runs.html", run=runs, prev_run=prev_run)