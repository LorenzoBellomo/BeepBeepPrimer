from flask import Blueprint, render_template, request, redirect

from stravalib import Client

from monolith.database import db, Run, User, Objectives, _setObjective
from monolith.auth import current_user
from monolith.forms import ObjectiveForm
from monolith.views.auth import *
from monolith.views.util import *

objective = Blueprint('objective', __name__)

@objective.route('/objective', methods=['GET', 'POST'])
def set_objective():
    form = ObjectiveForm()

    if form.validate_on_submit():
        objective_distance = km2m(form.data['distance'])
        q = db.session.query(User).filter(User.email == current_user.email)
        user = q.first()

        existing_objective = db.session.query(Objectives).filter(Objectives.user == user).first()
        if existing_objective is None:
            _setObjective(user, objective_distance)

        else:
            existing_objective.set_distance(objective_distance)

        db.session.commit()
        return redirect("/")

    return render_template('set_objective.html', form = form)