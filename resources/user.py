from flask_restful import Resource, reqparse
from models.user import UserModel

from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, 
    get_jwt_identity
)
from passlib.hash import sha256_crypt

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
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be blank."
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        
        if UserModel.find_by_id(data['id']):
            return {"message": "A user with that id already exists"}, 400

        password_hash_1 = sha256_crypt.encrypt(data['password'])
        user = UserModel(data['id'], data['email'], password_hash_1)
        user.save_to_db()

        # Identity can be any data that is json serializable
        access_token = create_access_token(identity=data['id'])
        refresh_token = create_refresh_token(identity=data['id'])
        return {"access_token": access_token,
                "refresh_token": refresh_token,
               "message": "User created successfully."}, 201

class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be blank."
    )

    def post(self):
        data = UserLogin.parser.parse_args()
        find_user = UserModel.find_by_email(data['email'])
        if find_user:
            # user with this email exists, check password
            if sha256_crypt.verify(data['password'], find_user.password):
                # passwords match, log user in
                # Identity can be any data that is json serializable
                access_token = create_access_token(identity=find_user.uid)
                refresh_token = create_refresh_token(identity=find_user.uid)
                return {"access_token": access_token,
                        "refresh_token": refresh_token,
                        "message": "User log in successfull."}, 200

        return {"message": "Invalid Email or Password!"}, 400


class UserProfile(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be blank."
    )

    def post(self, user_id):
        data = UserProfile.parser.parse_args()

        if UserModel.find_by_id(user_id):
            return {"message": "A user with that id already exists"}, 400

        password_hash_1 = sha256_crypt.encrypt(data['password'])
        user = UserModel(user_id, data['email'], password_hash_1)
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
        else:
            return {'message': 'User with ' + user_id + ' uid does not exist'}
        return {'message': 'User deleted'}

    def put(self, user_id):
        data = UserProfile.parser.parse_args()
        user = UserModel.find_by_id(user_id)
        if user:
            # user exists, update
            user.uid = user_id
            user.email = data['email']

            password_hash_1 = sha256_crypt.encrypt(data['password'])
            user.password = password_hash_1
            
        else:
            # user dne, create new user
            password_hash_1 = sha256_crypt.encrypt(data['password'])
            user = UserModel(user_id, data['email'], password_hash_1)

        user.save_to_db()
        return {"updated/created user with id: ": user.uid}


class UserProfileList(Resource):
    #@jwt_required
    def get(self):
        current_user = get_jwt_identity()
        return {'user_profiles': list(map(lambda x: x.json(), UserModel.query.all()))}
        


