from google.appengine.ext import ndb

from handlers.base_handlers import BaseAction
from models import Group, Event
from utils import user_utils


class ProfileAction(BaseAction):
    def handle_post(self, user):
        userInfo = user_utils.get_account_info(user)
        userInfo.name = self.request.get("inputName")
        userInfo.nickname = self.request.get("inputNickname")
        userInfo.email = self.request.get("inputEmail")
        userInfo.phoneNumber = self.request.get("inputPhoneNumber")
        userInfo.put()
        self.redirect("/profile")

    
class AddGroupAction(BaseAction):
    def handle_post(self, user):
        new_group = Group(parent=user_utils.get_parent_key(user),
                      groupName = self.request.get("name"),
                      groupDescription = self.request.get("description"))
        new_group.put()
        self.redirect("/group?group_key=" + new_group.key.urlsafe())
        
class UpdateGroupAction(BaseAction):
  def handle_post(self, user):
    group_name = self.request.get('group_name')
    group_description = self.request.get('group_description')
    urlsafe_entity_key = self.request.get('group_entity_key')
    urlsafe_group_keys_to_add = self.request.get('group_keys_to_add')
    urlsafe_group_keys_to_remove = self.request.get('group_keys_to_remove')
 
    add_to_keys = urlsafe_group_keys_to_add.split(",")
    remove_from_keys = urlsafe_group_keys_to_remove.split(",")
 
    group_key = ndb.Key(urlsafe=urlsafe_entity_key)
    group = group_key.get()
    
    for add_to_key in add_to_keys:
      if len(add_to_key) > 0:
        friend = ndb.Key(urlsafe=add_to_key).get()
        group.members.append(friend.key)  

    for remove_from_key in remove_from_keys:
      if len(remove_from_key) > 0:
        friend = ndb.Key(urlsafe=remove_from_key).get()
        group.members.remove(friend.key)

    if group_name != group.groupName:
      group.groupName = group_name
    if group_description != group.groupDescription:
        group.groupDescription = group_description
        
    group.put()

    self.redirect("/events?group_key="+group.key.urlsafe())
    
class AddEventAction(BaseAction):
    def handle_post(self, user):
        new_event = Event(parent=user_utils.get_parent_key(user),
                      eventName = self.request.get("eventName"),
                      eventDescription = self.request.get("eventDescription"))
        new_event.put()
        
        group = ndb.Key(urlsafe=self.request.get("group_entity_key")).get()
        group.events.append(new_event.key)
        group.put()
        
        self.redirect("/event?event_key=" + new_event.key.urlsafe())
        
        
class UpdateEventAction(BaseAction):
  def handle_post(self, user):
    pass
        