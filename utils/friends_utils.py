from google.appengine.ext import ndb

from google.appengine.ext import ndb

import facebook
from models import User
from utils import user_utils


def get_friends_list_from_cookie(cookie):
#     userInfo = user_utils.get_account_info(user)
#     if cookie["access_token"] != userInfo.access_token:
#         userInfo.access_token = cookie["access_token"]
#         userInfo.put()
    graph = facebook.GraphAPI(cookie["access_token"])
    friends_list = graph.get_connections("me", "friends")['data']
    friends = []
    for friend in friends_list:
        person = User.get_by_id(str(friend["id"]), parent=user_utils.get_parent_key_from_facebookID(str(friend["id"])))
        friends.append(person)
    return friends

def get_friends_list_from_user(user):
    account_info = user_utils.get_account_info(user)
    friends = []
    for friend in account_info.friendList:
        friends.append(friend.get())
    return friends