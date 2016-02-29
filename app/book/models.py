from app import db

#Creating the Similar book Class for the switch from peewee to
#Sql-Alchemy using the MVC method
#This File is going to be the model
class BookToRent(db.Model):
    pass

class BookToRent(db.Model):
     """BookToRent model."""
     id  = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255),nullable=False)
     edition = db.Column(db.String(255), nullable= False)
    author = db.Column(db.String(255), nullable= False)
    #TODO: not sure how to convert this to Sql-al -JOE
    description = TextField()#needs converting
    isbn = db.Column(db.String(255), nullable= False)
    condition = ForeignKeyField(BookCondition, to_field='condition', related_name='book')#needs converting
    condition_comment = TextField(default="")#needs converting
    marks =db.Column(db.Boolean, default=False)
    username = db.Column(db.ForeignKeyConstraint(user.username))# my testing
    username = ForeignKeyField(User, to_field='username', related_name='book')#needs converting
    available = ForeignKeyField(BookStatus, to_field='status', related_name='book')#needs converting
    added = db.Column(db.DateTime,nullable=False,default= None)
    # image_path = CharField(max_length=255, unique=True)