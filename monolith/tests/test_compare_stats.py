from monolith.database import User, Run
from pyquery import PyQuery as pq
from monolith.forms import ComparisonsForm
import sys
from monolith.tests.utils import ensure_logged_in


def test_compare_stats(client, db_instance):

    # simulate login
    user = ensure_logged_in(client, db_instance)

    # generate some runs
    runs = []
    for i in ['1', '2']:
        run = Run()

        run.runner = user
        run.strava_id = i
        run.name = "Run " + i
        run.average_speed = float(i)
        run.elapsed_time = float(i)*float(i)*1000

        runs.append(run)

        db_instance.session.add(run)
    db_instance.session.commit()

    # route to comparisons page
    res = client.post(
        '/comparisons',
        data={
            'runs': ['1', '2']
        },
        follow_redirects=True
    )

    # parse html page
    html = pq(res.data)
    table = html("#comparison-table")
    trs = table("tr")

    # check number of rows equals given runs (2)
    assert len(trs) - 1 == 2

    # check html table shows correct results
    for i in range(1, len(trs)):
        tds = trs.eq(i)("td")
        assert runs[i-1].average_speed == tds[1].text.strip()
        assert runs[i-1].elapsed_time == tds[2].text.strip()
