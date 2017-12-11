import os
import psycopg2 # adapter fo PostgreSQL. used to set uri with username, password, etc.
from flask import Flask
from flask_restful import Api

from flask_jwt_extended import JWTManager

from resources.user import UserRegister, UserProfile, UserProfileList, UserLogin
from resources.chat_post import ChatPost, ChatPostList, UserChatPostList

app = Flask(__name__)
api = Api(app)

# in heroku get env db var, if not found, use our sqlite for testing in our local env
driver = 'postgresql+psycopg2://'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')



# FlaskSqlAlchemy know when object changed but not have saved to the db = turn off
# SQLAlchemy main library itself has a modification tracker
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Setup the Flask-JWT-Extended extension (The secret key is needed to keep the client-side sessions secure)
app.secret_key = os.environ.get('AI_CHAT_SECRET_KEY', 'testingSecret')
jwt = JWTManager(app)

# flask_jwt /auth
# jwt = JWT(app, authenticate, identity)  



# SqlAlchemy can create db for us
# Use flask decorator 
# before first request run: app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' unless it alread exists
@app.before_first_request
def create_tables():
    db.create_all() # only creates tables that it sees



# add resources
api.add_resource(ChatPost, '/chat-post/<string:user_query>')
api.add_resource(ChatPostList, '/chat-posts') 
api.add_resource(UserChatPostList, '/user-chat-posts/<string:user_id>')

api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserProfile, '/user-profile/<string:user_id>')
api.add_resource(UserProfileList, '/user-profiles')


if __name__ == '__main__':
	# avoid Circular imports
	# Our item and models, import db as well.
	# If we import db at top, and import models at top, we have a circular import
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
    # PORT 5432
