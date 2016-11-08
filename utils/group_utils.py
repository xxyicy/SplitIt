from google.appengine.ext import ndb

from models import Group
from utils import user_utils, event_utils


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
    expense_from_user_member_map = {}
    expense_to_user_member_map = {}
    members = []
    for event in events:
        event_expense_member_map = event_utils.get_expenses(event)
        if event.payer.urlsafe() == user.key.urlsafe():
            for event_member in event_expense_member_map:
                to = ndb.Key(urlsafe=event_member).get()
                if to not in members:
                    members.append(to)
                if event_member in expense_to_user_member_map:
                    expense_to_user_member_map[event_member] += event_expense_member_map[event_member]
                else:
                    expense_to_user_member_map[event_member] = event_expense_member_map[event_member]
        elif user.key.urlsafe() in event_expense_member_map:
            to_key = event.payer
            to = to_key.get()
            if to not in members:
                members.append(to)
            if to_key.urlsafe() in expense_from_user_member_map:
                expense_from_user_member_map[to_key.urlsafe()] += event_expense_member_map[user.key.urlsafe()];
            else:
                expense_from_user_member_map[to_key.urlsafe()] = event_expense_member_map[user.key.urlsafe()];
    return members, expense_from_user_member_map, expense_to_user_member_map

