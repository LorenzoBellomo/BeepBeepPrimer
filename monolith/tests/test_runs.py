import unittest, json
from flask import request, jsonify
from monolith.app import create_app
from monolith.tests.utils import ensure_logged_in
from monolith.views.runs import _runs
from flask import Blueprint, render_template
from monolith.database import db, Run, User, _delete_user
from monolith.auth import current_user
from werkzeug import ImmutableMultiDict
import random


#if any of runs were deleted
def test_runs1(client, db_instance):
	# simulate login
	example = ensure_logged_in(client, db_instance)

	runs_id =['1', '2', '3', '4', '5', '6', '7']

	db.session.add(example)

	for i in runs_id:
		run = Run()
		run.runner = example
		run.strava_id = i
		run.name = "Run " + i
		run.average_speed = float(i)
		run.distance = 2000
		run.elapsed_time = float(i)*float(i)*1000
		db_instance.session.add(run)
	
	db.session.commit()
	user_id = example.get_id()


	previous_run = db.session.query(Run).filter(Run.runner_id == example.get_id(), Run.id<7).order_by(Run.id.desc()).first()
	assert previous_run.id == 6

	q = db.session.query(Run).filter(Run.runner_id == example.get_id(), Run.id == 4)
	q.delete(synchronize_session=False)
	db.session.commit()
	previous_run = db.session.query(Run).filter(Run.runner_id == example.get_id(), Run.id<5).order_by(Run.id.desc()).first()
	assert previous_run.id == 3
		


#if given id is larger than all run's  id
def test_runs2(client, db_instance):
	# simulate login
	example = ensure_logged_in(client, db_instance)

	runs_id =['1', '2', '3', '4', '5', '6', '7']

	db.session.add(example)

	for i in runs_id:
		run = Run()
		run.runner = example
		run.strava_id = i
		run.name = "Run " + i
		run.average_speed = float(i)
		run.distance = 2000
		run.elapsed_time = float(i)*float(i)*1000
		db_instance.session.add(run)
	
	db.session.commit()
	user_id = example.get_id()

	runId=150

	run = db.session.query(Run).filter(Run.runner_id == example.get_id(), Run.id == runId).first()
	assert run == None