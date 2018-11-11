from monolith.app import create_testing_app
from monolith.database import Run, User, _delete_user
import random


#if any of runs were deleted
def test_runs1(db_instance):
	email = 'mock' + str(random.randint(1, 101)) + '@mock.com'
	password = 'mock'
	example = User()
	example.email = email
	example.set_password(password)


	runs_id =['1', '2', '3', '4', '5', '6', '7']

	db_instance.session.add(example)

	for i in runs_id:
		run = Run()
		run.runner = example
		run.strava_id = i
		db_instance.session.add(run)
	
	db_instance.session.commit()
	user_id = example.get_id()


	previous_run = db_instance.session.query(Run).filter(Run.runner_id == example.get_id(), Run.id<7).order_by(Run.id.desc()).first()
	assert previous_run.id == 6

	q = db_instance.session.query(Run).filter(Run.runner_id == example.get_id(), Run.id == 4)
	q.delete(synchronize_session=False)
	db_instance.session.commit()
	previous_run = db_instance.session.query(Run).filter(Run.runner_id == example.get_id(), Run.id<5).order_by(Run.id.desc()).first()
	assert previous_run.id == 3

	_delete_user(example)
		


#if given id is larger than all run's  id
def test_runs2(db_instance):
	email = 'mock' + str(random.randint(1, 101)) + '@mock.com'
	password = 'mock'
	example = User()
	example.email = email
	example.set_password(password)


	runs_id =['1', '2', '3', '4', '5', '6', '7']

	
	db_instance.session.add(example)

	for i in runs_id:
		run = Run()
		run.runner = example
		run.strava_id = i
		db_instance.session.add(run)
	
	db_instance.session.commit()
	user_id = example.get_id()
	runId=150

	run = db_instance.session.query(Run).filter(Run.runner_id == example.get_id(), Run.id == runId).first()
	assert run == None

	_delete_user(example)
