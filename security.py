from werkzeug.security import safe_str_cmp
from models.user import UserModel

def authenticate(id, email):
	# check if uid exists in db (if yes, then user is registered with firebase)

    user = UserModel.find_by_id(id)
    if user:
    	return user
    # if user and safe_str_cmp(user.password, password):
    #     return user

# @params: payload is the contents of the jwt toekn
def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
