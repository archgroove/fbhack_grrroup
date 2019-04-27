from app import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    facebook_details = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


TASK_STATUSES = [
    'exists',
    'assigned',
    'awaits_approval',
    'approved'
]


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, unique=True, nullable=False)
    assigned_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    color = db.Column(db.String(10), unique=False, nullable=False)
