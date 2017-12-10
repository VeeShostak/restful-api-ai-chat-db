from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('email',
        type=str,
        required=True,
        help="This field cannot be blank."
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        
        if UserModel.find_by_id(data['id']):
            return {"message": "A user with that id already exists"}, 400

        user = UserModel(data['id'], data['email'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201



class UserProfile(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',
        type=str,
        required=True,
        help="This field cannot be blank."
    )

    def post(self, user_id):
        data = UserProfile.parser.parse_args()

        if UserModel.find_by_id(user_id):
            return {"message": "A user with that id already exists"}, 400

        user = UserModel(user_id, data['email'])
        # can unpack and pass it in as:
        #user = UserModel(data['username'], data['password'])
        
        user.save_to_db()

        return {"message": "User created successfully."}, 201


    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            return user.json()
        return {'message': 'User not found'}, 404

    def delete(self, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_from_db()
        return {'message': 'User deleted'}

    def put(self, user_id):
        data = UserProfile.parser.parse_args()
        user = UserModel.find_by_id(user_id)
        if user:
            # user exists, update
            user.uid = user_id
            user.email = data['email']
            
        else:
            # user dne, create new user
            user = UserModel(user_id, data['email'])

        user.save_to_db()
        return {"updated/created user with id: ": user.uid}

        
class UserProfileList(Resource):
    def get(self):
        return {'user_profiles': list(map(lambda x: x.json(), UserModel.query.all()))}
        


