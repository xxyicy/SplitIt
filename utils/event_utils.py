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

def get_expenses(event):
    