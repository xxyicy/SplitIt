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
    return members;