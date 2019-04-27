from app import db
from models import User, Task

db.create_all()

u = User(
        facebook_details='userid123',
        email='tomkunc0@gmail.com',
        name='Tom Kunc'
    )

u2 = User(
        facebook_details='userid456',
        email='Claire@gmail.com',
        name='Claire'
    )

for user in [u, u2]:
    db.session.add(user)

db.session.commit()

t = Task(
    name='Complete Grrroup',
    description='Let us get this Hackathon done!',
    assigned_id=u.id,
    status='exists',
    color='0000ff'
)
db.session.add(t)

db.session.commit()

