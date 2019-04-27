from app import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    facebook_details = db.Column(db.String(80), unique=True, nullable=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    avatar = db.Column(db.String(240), unique=False, nullable=True)

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
    description = db.Column(db.Text, unique=False, nullable=False)
    assignee = db.relationship('User', backref=db.backref('tasks', lazy=True))
    assigned_id = db.Column(db.ForeignKey('user.id'), nullable=True)
    status = db.Column(db.String(20), nullable=False)
    color = db.Column(db.String(10), unique=False, nullable=False)
