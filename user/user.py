import datetime

from models import User, db


def create_user(**kwargs):
    """Create user control."""
    db.connect()
    User.create(
        first_name=kwargs['first_name'],
        second_name=kwargs['second_name'],
        username=kwargs['username'],
        password=kwargs['password'],
        joined=datetime.datetime.now,
        university_name=kwargs['university_name'],
        university_email=kwargs['university_email'],
        personal_email=kwargs['personal_email'],
    )
    db.close()


if __name__ == '__main__':
    create_user(
        first_name='Daniel',
        second_name='Santos',
        username='dsantos',
        password='test',
        university_name='UML',
        university_email='daniel_santos@student.uml.edu',
        personal_email='dsantosp12@gmail.com'
    )
