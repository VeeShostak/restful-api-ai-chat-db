from flask import Flask
from flask_restful import Api

from flask_jwt import JWT

from security import authenticate, identity

from resources.user import UserRegister, UserProfile, UserProfileList
from resources.chat_post import ChatPost, ChatPostList, UserChatPostList

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# FlaskSqlAlchemy know when object changed but not have saved to the db = turn off
# SQLAlchemy main library itself has a modification tracker
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# TODO: HIDE SECRET KEY
app.secret_key = 'werete'
api = Api(app)

# SqlAlchemy can create db for us
# Use flask decorator 
# before first request run: app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' unless it alread exists
@app.before_first_request
def create_tables():
    db.create_all() # only creates tables that it sees

# /auth
# check if uid exists in db
jwt = JWT(app, authenticate, identity)  

# add resources
#api.add_resource(ChatPost, '/chat-post/<string:name>')
api.add_resource(ChatPost, '/chat-post')
api.add_resource(ChatPostList, '/chat-posts') 
api.add_resource(UserChatPostList, '/user-chat-posts/<string:name>')

api.add_resource(UserRegister, '/register')
api.add_resource(UserProfile, '/user-profile')
api.add_resource(UserProfileList, '/user-profiles')




if __name__ == '__main__':
	# avoid Circular imports
	# Our item and models, import db as well.
	# If we import db at top, and import models at top, we have a circular import
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
