from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """Represents an admin user for the management panel."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Grade(db.Model):
    """Represents a school grade and its homework calendar URL."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    calendar_url = db.Column(db.String(255), nullable=False)
    subscriptions = db.relationship('Subscription', backref='grade', lazy=True)

    def __repr__(self):
        return f'<Grade {self.name}>'

class Subscription(db.Model):
    """Represents a customer's subscription to a specific grade's homework."""
    id = db.Column(db.Integer, primary_key=True)
    whatsapp_number = db.Column(db.String(20), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    grade_id = db.Column(db.Integer, db.ForeignKey('grade.id'), nullable=False)

    # This will be populated by Wompi after the first successful payment
    wompi_payment_source_id = db.Column(db.String(100), nullable=True)

    subscription_start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    subscription_end_date = db.Column(db.DateTime, nullable=False)

    # Possible statuses: 'pending', 'active', 'past_due', 'cancelled'
    status = db.Column(db.String(20), nullable=False, default='pending')

    def __repr__(self):
        return f'<Subscription {self.whatsapp_number} for Grade {self.grade.name}>'
