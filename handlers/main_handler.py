import facebook
from google.appengine.ext import ndb
from handlers.base_handlers import BaseHandler, FACEBOOK_APP_ID, BasePage, \
    FACEBOOK_APP_SECRET
from models import Group
from utils import friends_utils, user_utils, group_utils, event_utils


class HomeHandler(BaseHandler):
    def update_values(self, user, values):
        if user:
            values["current_user"] = user

            groups = group_utils.get_groups(user)
            values["groups"] = groups
             
            group_member_map = {}
            friends = friends_utils.get_friends_list_from_user(user)
            for group in groups:
                group_member_map[group.key.urlsafe()] = ""
                current_member = ""
                for friend in friends:
                    if friend.key in group.members:
                        if current_member != "":
                            current_member += ","
                        current_member += friend.nickname
                group_member_map[group.key.urlsafe()] = current_member 
            values["group_member_map"] = group_member_map
            
            group_event_map = {}
 
    def get_template(self):
        if self.current_user:
            return "templates/groups.html"
        else:
            return "templates/base_page.html"    
         
        
class LogoutHandler(BaseHandler):
    def get(self):
        if "user" in self.session:
            del self.session['user']
        self.redirect(uri="/")

        
class FriendsHandler(BasePage):
    def get_template(self):
        return "templates/friends_list.html"    

    def update_values(self, user, values):
        cookie = facebook.get_user_from_cookie(self.request.cookies, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
        friend_list = friends_utils.get_friends_list_from_cookie(cookie)
        values["friends_list"] = friend_list
        
        account_info = user_utils.get_account_info(user)
        
        for friend in friend_list:
            if friend.key not in account_info.friendList:
                account_info.friendList.append(friend.key)
        account_info.put()

class ProfileHandler(BasePage):
    
    def get_template(self):
        return "templates/profile.html"
    
    
class GroupDetailHandler(BasePage):
    
    def get_template(self):
        return "templates/group.html"
    
    def update_values(self, user, values):
        group = ndb.Key(urlsafe=self.request.get('group_key')).get()
        friends = friends_utils.get_friends_list_from_user(user)
        friends_in_group = []
        friends_not_in_group = []
        for friend in friends:
          if friend.key in group.members:
            friends_in_group.append(friend)
          else:
            friends_not_in_group.append(friend)
        values["group"] = group
        values["friends_in_group"] = friends_in_group
        values["friends_not_in_group"] = friends_not_in_group
    
        
class EventsHandler(BasePage):
    def get_template(self):
        return "templates/events.html"
        
    def update_values(self, user, values):
        group = ndb.Key(urlsafe=self.request.get('group_key')).get()
        
        events = event_utils.get_events_from_group(user, group)
            
        event_member_map = {}
        
        friends = group_utils.get_members_exclude_user(user, group)
        for event in events:
            event_member_map[event.key.urlsafe()] = ""
            current_member = ""
            for friend in friends:
                if friend.key in event.members:
                    if current_member != "":
                        current_member += ","
                    current_member += friend.nickname
            event_member_map[event.key.urlsafe()] = current_member 
            
        values["group"] = group
        values["events"] = events
        values["event_member_map"] = event_member_map
        
        
class EventDetailHandler(BasePage):
    def get_template(self):
        return "templates/event.html"
        
    def update_values(self, user, values):
        userInfo = user_utils.get_account_info(user)
        event = ndb.Key(urlsafe=self.request.get('event_key')).get()
        group = ndb.Key(urlsafe=self.request.get('group_key')).get()
        friends = group_utils.get_members_exclude_user(user,group)
        friends_in_event = []
        friends_not_in_event = []
        for friend in friends:
          if friend.key in event.members:
            friends_in_event.append(friend)
          else:
            friends_not_in_event.append(friend)
            
        expenses=[]
        for expense in event.expenses:
            expenses.append(expense.get())
            
        values["event"] = event
        values["user"] = userInfo
        values["expenses"] = expenses
        values["friends_in_event"] = friends_in_event
        values["friends_not_in_event"] = friends_not_in_event
