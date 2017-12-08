from db import db
from datetime import datetime

# Tell SQLAlchemy this is an object we want to map by inheriting db.Model
# (Things we will be able to retrieve and send to db)


# NOTE: the 2 classmethods are an interface for another part of of our
# program to interact with the user (writing and retriveing from db)
# (security file uses this interface to commuincate with the user in db)
class UserModel(db.Model):
    # tell SQLAlchemy table name
    __tablename__ = 'users'

    # tell SQLAlchemy what columns we want the table to contain
    # id auto incremented
    id = db.Column(db.String(), primary_key=True)
    email = db.Column(db.String(200))
    created_at = db.Column(db.TIMESTAMP(timezone=True))


    # One to Many bidirectional (one user has many chatposts)
    
    # (establishment of an event listener on both sides which will mirror attribute operations in both directions
    # “when an append or set event occurs here, set ourselves onto the incoming attribute using this particular attribute name”.)
    
    # dynamic: enable management of a large collection using a dynamic relationship. 
    # returns a Query object in place of a collection.  filter() criterion may be applied as well as limits and offsets
    # ex: do not go into chat_posts table and do not load each object for each table unless we specify (use self.chat_posts.all() instead of self.chat_posts)
    chat_posts = db.relationship('ChatPostModel', back_populates='user_id', lazy='dynamic')

    # =========================================

    def __init__(self, id, email):
        self.id = id
        self.email = email

        #self.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.created_at = datetime.utcnow()

    # calling json() method is slow when calling self.chat_posts.all() due to lazy='dynamic' relationship
    def json(self):
        return {'id': self.id, 'email': self.email, 'chat_posts': [chat_posts.json() for chat_post in self.chat_posts.all()]}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        # get first row (sqlAlchemy then converts it to user model object)
        return cls.query.filter_by(email=email).first()

    # id is a built in python method, so name it _id
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
