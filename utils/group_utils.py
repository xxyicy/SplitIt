from models import Group
from utils import user_utils


def get_groups(user):
    return Group.query(ancestor=user_utils.get_parent_key(user)).order(Group.groupName).fetch()