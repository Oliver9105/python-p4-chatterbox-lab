from datetime import datetime
from app import app
from models import db, Message

class TestMessage:
    '''Message model in models.py'''

    def setup_method(self, method):
        with app.app_context():
            db.create_all()
            message = Message(body="Hello 👋", username="Liza")
            db.session.add(message)
            db.session.commit()

    def teardown_method(self, method):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_has_correct_columns(self):
        '''has columns for message body, username, and creation time.'''
        with app.app_context():
            hello_from_liza = Message.query.first()
            assert hello_from_liza.body == "Hello 👋"
            assert hello_from_liza.username == "Liza"
            assert type(hello_from_liza.created_at) == datetime
