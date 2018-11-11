from monolith.database import User, Objectives, Run, _setObjective
from monolith.views.util import km2m
from pyquery import PyQuery as pq
from utils import create_mock_user, ensure_logged_in

def test_objective(client, db_instance):

    #create fake user
    create_mock_user(client)

    #retreve the fake user
    user = db_instance.session.query(User).first()
    db_instance.session.add(user)

    #create 2 fake runs
    runs_id = ['1', '2']
    for i in runs_id:
        run = Run()
        run.runner = user
        run.strava_id = i
        run.distance = 1000
        run.average_speed = 10
        run.elapsed_time= 10000
        db_instance.session.add(run)

    db_instance.session.commit()

    #set objective
    objective_distance = 1000
    _setObjective(user, objective_distance)

    #check that the objective is correctly settend in the database
    assert db_instance.session.query(Objectives).first().distance == 1000

    # simulate login
    user = ensure_logged_in(client, db_instance)

    #check that the objective is correctly showed in the view
    res = client.get('/')
    html = pq(res.data)


    objective_view = km2m(float(html("#obj_dist").html()))    

    #check the view converting the distance to km
    assert objective_view == objective_distance