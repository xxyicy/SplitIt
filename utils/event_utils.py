def get_events_from_group(user, group):
    events_in_group = []
    friends = []
    for event in group.events:
        event_in_group = event.get()
        events_in_group.append(event_in_group)
    return events_in_group