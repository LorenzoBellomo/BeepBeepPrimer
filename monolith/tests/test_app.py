import unittest, os

from flask import request,Flask
from monolith.app import create_app
from monolith.database import db, Run, User
from monolith.views import blueprints
from monolith.auth import login_manager
from werkzeug import ImmutableMultiDict




class TestApp(unittest.TestCase):

	#check for first admin user
	def test_app1(self):
		app = create_app()
		with app.app_context():
			q = db.session.query(User).filter(User.email == 'example@example.com').first()
	
			self.assertEqual(q.email, 'example@example.com')
			self.assertEqual(q.is_admin, True)

