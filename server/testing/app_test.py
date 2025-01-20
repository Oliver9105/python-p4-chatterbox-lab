from datetime import datetime
from app import app
from models import db, Message

class TestApp:
    '''Flask application in app.py'''

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
        with app.app_context():
            hello_from_liza = Message.query.first()
            assert(hello_from_liza.body == "Hello 👋")
            assert(hello_from_liza.username == "Liza")
            assert(type(hello_from_liza.created_at) == datetime)

    def test_returns_list_of_json_objects_for_all_messages_in_database(self):
        '''returns a list of JSON objects for all messages in the database.'''
        with app.app_context():
            response = app.test_client().get('/messages')
            records = Message.query.all()
            for message in response.get_json():
                assert(message['id'] in [record.id for record in records])
                assert(message['body'] in [record.body for record in records])

    def test_creates_new_message_in_the_database(self):
        '''creates a new message in the database.'''
        with app.app_context():
            app.test_client().post(
                '/messages',
                json={
                    "body":"Hello 👋",
                    "username":"Liza",
                }
            )
            h = Message.query.filter_by(body="Hello 👋").first()
            assert(h)
            db.session.delete(h)
            db.session.commit()

    def test_returns_data_for_newly_created_message_as_json(self):
        '''returns data for the newly created message as JSON.'''
        with app.app_context():
            response = app.test_client().post(
                '/messages',
                json={
                    "body":"Hello 👋",
                    "username":"Liza",
                }
            )
            assert(response.content_type == 'application/json')
            assert(response.json["body"] == "Hello 👋")
            assert(response.json["username"] == "Liza")

            h = Message.query.filter_by(body="Hello 👋").first()
            assert(h)
            db.session.delete(h)
            db.session.commit()

    def test_updates_body_of_message_in_database(self):
        '''updates the body of a message in the database.'''
        with app.app_context():
            m = Message.query.first()
            id = m.id
            response = app.test_client().patch(f'/messages/{id}', json={'body': 'Updated body'})
            assert response.status_code == 200
            assert response.get_json()['body'] == 'Updated body'

    def test_returns_data_for_updated_message_as_json(self):
        '''returns data for the updated message as JSON.'''
        with app.app_context():
            m = Message.query.first()
            id = m.id
            response = app.test_client().patch(f'/messages/{id}', json={'body': 'Updated body'})
            assert response.status_code == 200
            assert response.get_json()['body'] == 'Updated body'

    def test_deletes_message_from_database(self):
        '''deletes the message from the database.'''
        with app.app_context():
            hello_from_liza = Message(
                body="Hello 👋",
                username="Liza"
            )
            db.session.add(hello_from_liza)
            db.session.commit()

            response = app.test_client().delete(
                f'/messages/{hello_from_liza.id}'
            )

            assert response.status_code == 200  # Ensure the delete request was successful

            h = db.session.get(Message, hello_from_liza.id)
            assert not h  # Ensure the message is deleted
