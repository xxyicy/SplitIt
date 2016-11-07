from models import Expense
from utils import user_utils


def get_events_from_group(user, group):
    events_in_group = []
    friends = []
    for event in group.events:
        event_in_group = event.get()
        events_in_group.append(event_in_group)
    return events_in_group

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