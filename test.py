from app.user.user import UserController

UserController.create_user(first_name="Daniel",
                           last_name="Santos",
                           username="Test",
                           password="Powlaadfasdf",
                           university_email="dsadsA@dasdfa.com"
                           )

myController = UserController("Daniel", "Santos", "dsantosp2", "test")

myController.create()
