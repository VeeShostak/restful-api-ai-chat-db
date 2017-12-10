from db import db
from datetime import datetime

class ChatPostModel(db.Model):
    __tablename__ = 'user_chat_posts'

    id = db.Column(db.Integer, primary_key=True) # auto incr PK ChatPost Id
    user_query = db.Column(db.String(200))
    response = db.Column(db.String(200))
    machine_responded = db.Column(db.Boolean())
    created_at = db.Column(db.TIMESTAMP(timezone=True))

    # Bidirectional - ManyToOne - many chatPosts to one user
    # know what user the chatPost belongs to
    # (establishment of an event listener on both sides which will mirror attribute operations in both directions
    # “when an append or set event occurs here, set ourselves onto the incoming attribute using this particular attribute name”.)
    user_id = db.Column(db.String(), db.ForeignKey('users.uid'))
    #user = db.relationship('UserModel')
    user = db.relationship('UserModel', back_populates='chat_posts', cascade='save-update, merge')
    # cascading: do not delete user if delete chat post (do not cascade on delete (default value of cascade is save-update, merge)
    # 

    # =========================================

    def __init__(self, user_query, response, machine_responded, user_id):
        self.user_query = user_query
        self.response = response
        self.machine_responded = machine_responded
        self.user_id = user_id

        #self.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.created_at = datetime.utcnow()

    def json(self):
        return {'id': self.id, 'user_query': self.user_query, 'response': self.response, 'machine_responded': self.machine_responded, 'created_at': self.created_at.strftime('%c'), 'user_id': self.user_id}

    @classmethod
    def find_by_user_query(cls, user_query):
        # SQLAlchemy:
        # SELECT * FROM items WHERE col=col LIMIT 1
        # LIMIT or .first() returns the first row only
        #returns a chatPost model object
        return cls.query.filter_by(user_query=user_query).first()

    # for update AND insert
    def save_to_db(self):
        # aession a collection of ojects we will write to the db
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
