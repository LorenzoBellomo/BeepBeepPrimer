from monolith.database import User

def test_app(db_instance):
	q = db_instance.session.query(User).filter(User.email == 'example@example.com').first()
	
	assert q.email == 'example@example.com'
	assert q.is_admin == True
