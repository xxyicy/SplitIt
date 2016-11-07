<<<<<<< HEAD
from google.appengine.ext import ndb

from handlers.base_handlers import BaseAction
from models import Group, Event
from utils import user_utils, friends_utils
import datetime
=======
import json

from google.appengine.ext import ndb
from handlers.base_handlers import BaseAction
from models import Group, Event
from utils import user_utils, friends_utils, event_utils

>>>>>>> master

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
                      groupName=self.request.get("name"),
                      groupDescription=self.request.get("description"),
                      members=[user_utils.get_account_info(user).key])
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
        friend = ndb.Key(urlsafe=add_to_key)
        group.members.append(friend)  

    for remove_from_key in remove_from_keys:
      if len(remove_from_key) > 0:
        friend = ndb.Key(urlsafe=remove_from_key)
        group.members.remove(friend)

    if group_name != group.groupName:
      group.groupName = group_name
    if group_description != group.groupDescription:
        group.groupDescription = group_description
        
    group.put()

    self.redirect("/events?group_key=" + group.key.urlsafe())
    
<<<<<<< HEAD
class FinishGroupAction(BaseAction):
    def handle_post(self, user):
        group_key = self.request.get("group_key")
        group = ndb.Key(urlsafe=group_key).get()
        group.finished = True
        group.finishDate = datetime.datetime.now()
        group.put()
        
        self.redirect("/")
    
class AddEventAction(BaseAction):
    def handle_post(self, user):
        new_event = Event(parent=user_utils.get_parent_key(user),
                      eventName=self.request.get("eventName"),
                      eventDescription=self.request.get("eventDescription"))
=======
class AddEventAction(BaseAction):
    def handle_post(self, user):
        userInfo = user_utils.get_account_info(user)
        event_totalCost = self.request.get("eventTotalCost")
        if not event_totalCost:
            event_totalCost = 0
        new_event = Event(parent=user_utils.get_parent_key(user),
                      eventName=self.request.get("eventName"),
                      eventDescription=self.request.get("eventDescription"),
                      payer=userInfo.key,
                      totalCost=float(event_totalCost),
                      group_key=self.request.get("group_entity_key"))
>>>>>>> master
        new_event.put()
        
        group_key = ndb.Key(urlsafe=self.request.get("group_entity_key"))
        group = group_key.get()
        group.events.append(new_event.key)
        group.put()
        
        self.redirect("/event?event_key=" + new_event.key.urlsafe() + "&group_key=" + group_key.urlsafe())
        
        
class UpdateEventAction(BaseAction):
  def handle_post(self, user):
<<<<<<< HEAD
    # TODO: update event from db and get group_key     
    group_key = ""
    self.redirect("/events?group_key=" + group_key)
=======
    # TODO: update event from db and get group_key
#     blob = self.request.get('json')
#     data = json.loads(self.request.body)  
    event_name = self.request.get('event_name')
    event_description = self.request.get('event_description')
    event_totalCost = self.request.get('event_totalCost')
    if not event_totalCost:
        event_totalCost = 0
    urlsafe_entity_key = self.request.get('event_entity_key')
    urlsafe_event_keys_to_add = self.request.get('event_keys_to_add')
    urlsafe_event_keys_to_remove = self.request.get('event_keys_to_remove')
    expenses_String = self.request.get_all("expenses")
    expenses = json.loads(expenses_String[0])
        
    event_key = ndb.Key(urlsafe=urlsafe_entity_key)
    event = event_key.get()
      
    add_to_keys = urlsafe_event_keys_to_add.split(",")
    remove_from_keys = urlsafe_event_keys_to_remove.split(",")

    for expense in expenses:
        if expense["expense_key"] != "none":
            exp = ndb.Key(urlsafe=expense["expense_key"]).get()
            exp.cost = float(expense["cost"])
            exp.put()
       
    for add_to_key in add_to_keys:
        if len(add_to_key) > 0:
            friend = ndb.Key(urlsafe=add_to_key)
            event.members.append(friend)
            event_utils.add_user_expense_to_event(friend.get(), event, expenses)
    
    for remove_from_key in remove_from_keys:
        if len(remove_from_key) > 0:
            friend = ndb.Key(urlsafe=remove_from_key)
            event.members.remove(friend)
            event_utils.delete_user_expense_from_event(friend.get(), event)
       
    if event_name != event.eventName:
        event.eventName = event_name
    if event_description != event.eventDescription:
        event.groupDescription = event_description
    if event_totalCost != str(event.totalCost):
        event.totalCost = float(event_totalCost)
           
    event.put()
         
#     group_key = event.group_key
#      self.redirect("/events?group_key=" + group_key)
    self.response.headers['Content-Type'] = 'application/json'   
    obj = {"event_name": event_name,
                "event_description": event_description,
                "event_totalCost": event_totalCost,
                "event_entity_key": urlsafe_entity_key,
                "event_keys_to_add": urlsafe_event_keys_to_add,
                "event_keys_to_remove": urlsafe_event_keys_to_remove,
                "expenses": expenses}
    self.response.out.write(json.dumps(obj))
>>>>>>> master
        
