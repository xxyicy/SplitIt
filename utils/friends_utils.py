
import facebook
from models import User
from utils import user_utils


def get_friends_list_from_user(user):
    graph = facebook.GraphAPI(user["access_token"])
    friends_list = graph.get_connections("me", "friends")['data']
    friends = []
    for friend in friends_list:
        person = User.get_by_id(str(friend["id"]), parent=user_utils.get_parent_key_from_facebookID(str(friend["id"])))
        friends.append(person)
    return friends