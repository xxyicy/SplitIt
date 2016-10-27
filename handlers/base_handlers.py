from email import email
import hashlib
import json
import logging
import os
import urllib2
import wsgiref.handlers

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
import jinja2
import webapp2
from webapp2_extras import sessions

import facebook
import main
from models import User
from utils import user_utils


FACEBOOK_APP_ID = "1362095630475570"  # your own FB app id here
FACEBOOK_APP_SECRET = "6e9760b0cc49fd736a9b36998aad064e"  # your own FB app secret here
INVITATION_TEXT = "I invite you to try my app. It is amazing!"


class BasePage(webapp2.RequestHandler):
  """Page handlers should inherit from this one."""
  def get(self):
    template = main.jinja_env.get_template(self.get_template())
    user = self.current_user
    self.handle_get(user)
    values = {}
    values = self.update_values(user, values)
    self.response.out.write(template.render(values))
    
    
  def post(self):
    template = main.jinja_env.get_template(self.get_template())
    user = self.current_user
    self.handle_post(user)
    values = {}
    values = self.update_values(user, values)
    self.response.out.write(template.render(values))
      
    
  def update_values(self, user, values):
    # Subclasses should override this method to add additional data.
    pass

  def get_template(self):
    # Subclasses must override this method to set the Jinja template.
    raise Exception("Subclass must implement handle_post!")
    pass
  
  def handle_get(self, user):
      pass
  
  def handle_post(self, user):
      pass
  

  @property
  def current_user(self):
    if "user" not in self.session:
        cookie = facebook.get_user_from_cookie(self.request.cookies, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
        if cookie:
        # Store a local instance of the user data so we don't need
        # a round-trip to Facebook on every request
            graph = facebook.GraphAPI(cookie["access_token"])
            profile = graph.get_object("me?fields=email,id,name")
            user = User.get_by_id(str(profile["id"]), parent=user_utils.get_parent_key_from_facebookID(str(profile["id"])))
            if not user:
                user = User(parent=user_utils.get_parent_key_from_facebookID(str(profile["id"])),id=str(profile["id"]))
                user.name = profile["name"]
                user.username = profile["name"]
                user.access_token = cookie["access_token"]
                user.put()
            elif user.access_token != cookie["access_token"]:
                user.access_token = cookie["access_token"]
                user.put()
                 
            self.session["user"] = dict(
                    id=str(profile["id"]),
                    name=profile["name"],
                    access_token = cookie["access_token"])

            return self.session.get("user")
        else:
            return None
    return self.session.get("user")


  def dispatch(self):
    self.session_store = sessions.get_store(request=self.request)
    try:
        webapp2.RequestHandler.dispatch(self)
    finally:
        self.session_store.save_sessions(self.response)

  @webapp2.cached_property
  def session(self):
    return self.session_store.get_session()
    
class LoginPage(BasePage):
    def get(self):
        template = main.jinja_env.get_template(self.get_template())
        user = self.current_user
        self.handle_get(user)
        if user:
            values = {}
            values = self.update_values(user, values)
            self.response.out.write(template.render(values))
        else: 
            self.redirect("/")
            
    def post(self):
        template = main.jinja_env.get_template(self.get_template())
        user = self.current_user
        self.handle_post(user)
        if user:
            values = {}
            values = self.update_values(user, values)
            self.response.out.write(template.render(values))
        else: 
            self.redirect("/")
            
class BaseAction(webapp2.RequestHandler):
  """ALL action handlers should inherit from this one."""
  def post(self):
    pass
#     account_info = account_utils.get_account_info(user)
#     self.handle_post(user, account_info)

  def get(self):
    self.post()  # Just makes sure not subclasses try to make a simple quick and dirty page out of an Action.

  def handle_post(self, user, account_info):
    raise Exception("Subclass must implement handle_post!")

class HomeHandler(BasePage):
   
    def update_values(self, user, values):
        if user:
          return dict(current_user=user,
                            facebook_app_id=FACEBOOK_APP_ID)
        else:
            return dict(facebook_app_id=FACEBOOK_APP_ID)

        
        
    def get_template(self):
        return "templates/base_page.html"    
         
        
class LogoutHandler(BasePage):
    def get(self):
        if "user" in self.session:
            del self.session['user']
        self.redirect(uri="/")

        
class FriendsHandler(LoginPage):
    def get_template(self):
        return "templates/friends_list.html"    

    def update_values(self, user, values):
        return dict(current_user=user,
                        facebook_app_id=FACEBOOK_APP_ID,
                        friends_list= friends_utils.get_friends_list_from_user(user))
                 

class ProfileHandler(LoginPage):
    
    def handle_post(self, user):
        userInfo = user_utils.get_user_by_facebookID(user["id"])
        userInfo.name = self.request.get("inputName")
        userInfo.username = self.request.get("inputUsername")
        userInfo.email = self.request.get("inputEmail")
        userInfo.phoneNumber = self.request.get("inputPhoneNumber")
        userInfo.put()
        
    def get_template(self):
        return "templates/profile.html"
    
    def update_values(self, user, values):
        return dict(current_user= user_utils.get_user_by_facebookID(user["id"]),
                        facebook_app_id=FACEBOOK_APP_ID)
        
