from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)



@app.route('/')
def index():
    return "Welcome to the Chatterbox API!"

@app.route('/messages', methods=['GET', 'POST'])
def handle_messages():
    if request.method == 'GET':
        messages = [message.to_dict() for message in Message.query.order_by(Message.created_at.asc()).all()]
        return make_response(jsonify(messages), 200)

    elif request.method == 'POST':
        data = request.get_json()
        new_message = Message(
            body=data['body'],
            username=data['username'],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(new_message)
        db.session.commit()
        return make_response(jsonify(new_message.to_dict()), 201)

@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def handle_message(id):
    session = db.session 

    if request.method == 'GET':
        message = session.get(Message, id)
        return make_response(jsonify(message.to_dict()), 200)

    elif request.method == 'PATCH':
        data = request.get_json()
        message = session.get(Message, id)
        if 'body' in data:
            message.body = data['body']
        message.updated_at = datetime.utcnow()
        session.commit()
        return make_response(jsonify(message.to_dict()), 200)

    elif request.method == 'DELETE':
        message = session.get(Message, id)
        session.delete(message)
        session.commit()
        return make_response({"message": "Message deleted successfully"}, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
