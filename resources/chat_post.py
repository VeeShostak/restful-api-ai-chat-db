from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, jwt_refresh_token_required
from models.chat_post import ChatPostModel

class ChatPost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('response',
        type=str,
        required=True,
        help="chatPost missing a response"
    )
    parser.add_argument('machine_responded',
        type=bool,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('user_id',
        type=str,
        required=True,
        help="This field cannot be left blank, to which userId does this chatPost belong to"
    )

    @jwt_required
    def get(self, user_query):

        recievedChatPost = ChatPostModel.find_by_user_query(user_query)
        if recievedChatPost:
            return recievedChatPost.json()
        return {'message': 'chatPost with user query \'' + user_query + '\' not found'}, 404

    @jwt_refresh_token_required
    def post(self, user_query):

        data = ChatPost.parser.parse_args()

        recievedChatPost = ChatPostModel(user_query, data['response'], data['machine_responded'], data['user_id'])
        # or recievedChatPost = ChatPostModel(name, **data)

        try:
            recievedChatPost.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return recievedChatPost.json(), 201

    @jwt_refresh_token_required
    def put(self, user_query):

        data = ChatPost.parser.parse_args()
        recievedChatPost = ChatPostModel.find_by_user_query(user_query)

        if recievedChatPost:
            # update if exists
            recievedChatPost.user_query = user_query
            recievedChatPost.response = data['response']
            recievedChatPost.machine_responded = data['machine_responded']
            recievedChatPost.user_id = data['user_id']
        else:
            # create if dne
            recievedChatPost = ChatPostModel(user_query, data['response'], data['machine_responded'], data['user_id'])
        
        recievedChatPost.save_to_db()

        return recievedChatPost.json()

    @jwt_required
    def delete(self, user_query):

        recievedChatPost = ChatPostModel.find_by_user_query(user_query)

        if recievedChatPost:
            recievedChatPost.delete_from_db()

        return {'message': 'chatPost deleted'}


class ChatPostList(Resource):
    # list all chat posts
    @jwt_required
    def get(self):
        # apply   lambda x: x.json()   to each element in the list
        return {'ChatPosts': list(map(lambda x: x.json(), ChatPostModel.query.all()))}

        # list comprehension
        # return {'items': [item.json() for item in ItemModel.query.all()]}

class UserChatPostList(Resource):
    # list all chat posts of a specific user
    @jwt_required
    def get(self, user_id):

        # apply lambda x: x.json() to each element in the list
        return {'ChatPosts': list(map(lambda x: x.json(), ChatPostModel.query.filter_by(user_id=user_id)))}

