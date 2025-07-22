from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships (will define Pickup & Complaint models later)
    # All pickups *requested by* this user
    pickups_requested = db.relationship(
        'Pickup',
        foreign_keys='Pickup.user_id',
        backref='user',
        lazy=True
    )

    # All pickups *assigned to* this user as driver
    pickups_driven = db.relationship(
        'Pickup',
        foreign_keys='Pickup.driver_id',
        backref='driver',
        lazy=True
    )

    complaints = db.relationship('Complaint', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.username!r}, role={self.role!r}>"

class Pickup(db.Model):
    __tablename__ = 'pickups'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    pin_code = db.Column(db.String(10), nullable=False)
    waste_type = db.Column(db.String(20), nullable=False)
    pickup_date = db.Column(db.Date, nullable=False)
    time_slot = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Complaint(db.Model):
    __tablename__ = 'complaints'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    photo_path = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Complaint {self.id} by User {self.user_id}, status={self.status}>"
