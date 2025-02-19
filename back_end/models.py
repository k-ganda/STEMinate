from datetime import datetime
from .database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# ... other imports ... (if any)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    profile_picture = db.Column(db.String(128))
    bio = db.Column(db.String(255))
    conversations = db.relationship('Conversation', backref='creator', lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


def load_user(user_id):
    """
    This function retrieves a user object based on the provided user ID.
    """
    return User.query.get(int(user_id))  # Convert user_id to integer for database lookup

conversation_participants = db.Table('conversation_participants',
    db.Column('conversation_id', db.Integer, db.ForeignKey('conversation.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    participants = db.relationship('User', secondaryjoin='conversation_participants', backref='conversations')
    messages = db.relationship('Message', backref='conversation', lazy='dynamic')

    def __init__(self, participants):
        self.participants = participants

    def __repr__(self):
        return '<Conversation %r>' % self.id


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.String(1024))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))
    is_read = db.Column(db.Boolean, default=False)  # New field for read receipts

    def __repr__(self):
        return '<Message %r>' % self.id
