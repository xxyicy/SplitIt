from models import Group
from utils import user_utils


def get_groups(user):
    groups = Group.query().fetch()
    account_info = user_utils.get_account_info(user)
    groups_have_user = []
    for group in groups:
        if account_info.key in group.members:
            groups_have_user.append(group)
    return groups_have_user

def get_members_exclude_user(user,group):
    members = []
    account_info = user_utils.get_account_info(user)
    for member_key in group.members:
        if member_key != account_info.key:
            members.append(member_key.get())
<<<<<<< HEAD
    return members;

def get_members(user, group):
    members = []
    account_info = user_utils.get_account_info(user)
    for member_key in group.members:
        members.append(member_key.get())
    return members;

def get_friends_in_group(friends, group):
    friends_in_group = []
    for friend in friends:
      if friend.key in group.members:
        friends_in_group.append(friend)
    return friends_in_group

def get_friends_not_in_group(friends, group):
    friends_not_in_group = []
    for friend in friends:
      if friend.key not in group.members:
        friends_not_in_group.append(friend)
    return friends_not_in_group

def get_expenses_for_user(user, group):
    events = []
    for event_key in group.events:
        events.append(event_key.get())
    expense_map = {}
#     for event in events:
#         if user.key.urlsafe() != event.
    return expense_map
=======
    return members;
>>>>>>> master
