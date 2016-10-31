#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os

import jinja2
import webapp2
from webapp2_extras import sessions

from handlers import main_handler, insert_handlers, delete_handlers


jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                               autoescape=True)
# 
# class MainHandler(webapp2.RequestHandler):
#     def get(self):
#         template = jinja_env.get_template("templates/base_page.html")
#         self.response.write(template.render())
config = {}
config['webapp2_extras.sessions'] = {
    # This key is used to encrypt your sessions
    'secret_key': 'mysupersecretkey',
}

app = webapp2.WSGIApplication([
    ('/', main_handler.HomeHandler),
    ('/logout', main_handler.LogoutHandler),
    ('/friends', main_handler.FriendsHandler),
    ('/profile', main_handler.ProfileHandler),
    ('/group', main_handler.GroupDetailHandler),
    ('/events', main_handler.EventsHandler),
    ('/event', main_handler.EventDetailHandler),
    
    ('/edit-profile', insert_handlers.ProfileAction),
    ('/insert-group', insert_handlers.AddGroupAction),
    ('/update-group', insert_handlers.UpdateGroupAction),
    ('/insert-event', insert_handlers.AddEventAction),
    ('/update-event', insert_handlers.UpdateEventAction),
    
    ('/delete-group', delete_handlers.DeleteGroupAction),
    ('/delete-event', delete_handlers.DeleteEventAction),
], config=config, debug=True)
