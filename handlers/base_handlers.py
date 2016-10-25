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

from Model import User
import facebook
import main


FACEBOOK_APP_ID = "1362095630475570" #your own FB app id here
FACEBOOK_APP_SECRET = "6e9760b0cc49fd736a9b36998aad064e" #your own FB app secret here
INVITATION_TEXT = "I invite you to try my app. It is amazing!"


class BasePage(webapp2.RequestHandler):
  """Page handlers should inherit from this one."""
  def get(self):
    pass


  def update_values(self, user, values):
    # Subclasses should override this method to add additional data.
    pass

  def get_template(self):
    # Subclasses must override this method to set the Jinja template.
    raise Exception("Subclass must implement handle_post!")
    pass

  @property
  def current_user(self):
    if self.session.get("user"):
            # user is logged in
        return self.session.get("user")
    else: 
        cookie = facebook.get_user_from_cookie(self.request.cookies, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
        if cookie:
            # Store a local instance of the user data so we don't need
            # a round-trip to Facebook on every request
            graph = facebook.GraphAPI(cookie["access_token"])
            profile = graph.get_object("me")
            user = User.query(User.id==cookie["uid"]).get()
            if not user:
                user = User(id=str(profile["id"]),
                            name=profile["name"],
                            access_token=cookie["access_token"])
                print(profile.keys())
                user.put()
            elif user.access_token != cookie["access_token"]:
                user.access_token = cookie["access_token"]
                user.put()
                
            self.session["user"] = dict(
                    id = str(profile["id"]),
                    name=profile["name"],
                    access_token = cookie["access_token"]
                )
            return self.session.get("user")
        return None

  def dispatch(self):
    self.session_store = sessions.get_store(request=self.request)
    try:
        webapp2.RequestHandler.dispatch(self)
    finally:
        self.session_store.save_sessions(self.response)

  @webapp2.cached_property
  def session(self):
    return self.session_store.get_session()
    
class BaseAction(webapp2.RequestHandler):
  """ALL action handlers should inherit from this one."""
  def post(self):
    user = users.get_current_user()
    if not user:
      raise Exception("Missing user!")
#     account_info = account_utils.get_account_info(user)
#     self.handle_post(user, account_info)

  def get(self):
    self.post()  # Just makes sure not subclasses try to make a simple quick and dirty page out of an Action.

  def handle_post(self, user, account_info):
    raise Exception("Subclass must implement handle_post!")

class HomeHandler(BasePage):
    def get(self):
        self.show_main()
 
    def post(self):
        self.show_main()
         
    def show_main(self):
        template = main.jinja_env.get_template("templates/base_page.html")
        if "user" not in self.session:
            cookie = facebook.get_user_from_cookie(self.request.cookies, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
            if cookie:
            # Store a local instance of the user data so we don't need
            # a round-trip to Facebook on every request
                graph = facebook.GraphAPI(cookie["access_token"])
                profile = graph.get_object("me")
                user = User.query(User.id==cookie["uid"]).get()
                if not user:
                    user = User(id=str(profile["id"]),
                                name=profile["name"],
                                access_token=cookie["access_token"])
  
                    user.put()
                elif user.access_token != cookie["access_token"]:
                    user.access_token = cookie["access_token"]
                    user.put()
                
                self.session["user"] = dict(
                        id = str(profile["id"]),
                        name=profile["name"],
                        access_token = cookie["access_token"])
                self.redirect(uri="/")
            else:
                self.response.out.write(template.render({"facebook_app_id": FACEBOOK_APP_ID}))
#           args = dict(current_user=self.current_user,
#                     facebook_app_id=FACEBOOK_APP_ID)
#           self.response.out.write(template.render(args))
        else:
#           self.response.out.write(template.render({"facebook_app_id": FACEBOOK_APP_ID}))
          args = dict(current_user=self.session.get("user"),
                  facebook_app_id=FACEBOOK_APP_ID)
          self.response.out.write(template.render(args))
        
        
class LogoutHandler(BasePage):
    def get(self):
        del self.session["user"]
#         template = main.jinja_env.get_template("templates/logout.html")
#         user = self.session["user"]
#         self.response.out.write(template.render({"user": user}))
        self.redirect(uri="/")