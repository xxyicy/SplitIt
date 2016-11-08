from models import Expense
from utils import user_utils

def get_events_from_group(user, group):
    events_in_group = []
    friends = []
    for event in group.events:
        event_in_group = event.get()
        events_in_group.append(event_in_group)
    return events_in_group


def get_friends_in_event(friends, event):
    friends_in_event = []
    for friend in friends:
      if friend.key in event.members:
        friends_in_event.append(friend)
    return friends_in_event

def get_friends_not_in_event(friends, event):
    friends_not_in_event = []
    for friend in friends:
      if friend.key not in event.members:
        friends_not_in_event.append(friend)
    return friends_not_in_event
    
def delete_user_expense_from_event(user, event):
    expense_keys = event.expenses
    for expense_key in expense_keys:
        expense = expense_key.get()
        if user.key.urlsafe() == expense.person.urlsafe():
            expense_keys.remove(expense_key)
            expense_key.delete()
            break

def add_user_expense_to_event(user, event, expenses):
    for expense in expenses:
        if expense["person_key"] == user.key.urlsafe():
            exp = Expense(parent=user.key, person=user.key, cost=float(expense["cost"]), to=event.payer)
            exp.put()
    
#     expense = Expense(parent=user.key, person=user.key, cost=0)
#     expense.put()
    
    event.expenses.append(exp.key)
    event.put()
    
def get_expenses(event):
    event_expense_member_map = {}
    for expense_key in event.expenses:
        expense = expense_key.get()
        event_expense_member_map[expense.person.urlsafe()] = expense.cost
    return event_expense_member_map

