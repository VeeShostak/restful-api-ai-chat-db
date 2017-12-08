from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.chat_post import ChatPostModel

class ChatPost(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('user_query',
        type=str,
        required=True,
        help="chatPost missing a user_query"
    )
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



    # =================================================

    #@jwt_required()
    def get(self):

        data = ChatPost.parser.parse_args()
        recievedChatPost = ChatPostModel.find_by_user_query(data['user_query'])

        if recievedChatPost:
            return recievedChatPost.json()
        return {'message': 'chatPost with user query \'' + user_query + '\' not found'}, 404

    def post(self):

        # if ChatPostModel.find_by_user_query(user_query):
        #     return {'message': "An chatPost with user wueary '{}' already exists.".format(user_query)}, 400

        data = ChatPost.parser.parse_args()

        recievedChatPost = ChatPostModel(data['user_query'], data['response'], data['machine_responded'])
        # or item = ItemModel(name, **data)

        try:
            recievedChatPost.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return recievedChatPost.json(), 201

    def delete(self, name):

        data = ChatPost.parser.parse_args()
        recievedChatPost = ChatPostModel.find_by_user_query(data['user_query'])

        if recievedChatPost:
            recievedChatPost.delete_from_db()

        return {'message': 'chatPost deleted'}

    def put(self):

        data = ChatPost.parser.parse_args()
        recievedChatPost = ChatPostModel.find_by_user_query(data['user_query'])

        if recievedChatPost:
            # update if exists
            recievedChatPost.user_query = data['user_query']
            recievedChatPost.response = data['response']
            recievedChatPost.machine_responded = data['machine_responded']
        else:
            # create if dne
            recievedChatPost = ChatPostModel(data['user_query'], data['response'], data['machine_responded'])
            
        recievedChatPost.save_to_db()

        return recievedChatPost.json()


class ChatPostList(Resource):
    def get(self):
        # ChatPostModel.query.all() gives all object in table

        # apply   lambda x: x.json()   to each element in the list
        return {'ChatPosts': list(map(lambda x: x.json(), ChatPostModel.query.all()))}

        # list comprehension
        # return {'items': [item.json() for item in ItemModel.query.all()]}

class UserChatPostList(Resource):
    def get(self, user_id):

        #getChatPostList = ChatPostModel.get_all_with_uid(data['user_id'])

        # apply   lambda x: x.json()   to each element in the list
        return {'ChatPosts': list(map(lambda x: x.json(), ChatPostModel.query.filter_by(uid=id)))}

