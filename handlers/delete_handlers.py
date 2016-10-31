from google.appengine.ext import ndb

from handlers.base_handlers import BaseAction


class DeleteGroupAction(BaseAction):
  def handle_post(self, user):
      group_key = ndb.Key(urlsafe=self.request.get('group_to_delete_key'))
      group_key.delete();
      self.redirect("/")  
    
    
class DeleteEventAction(BaseAction):
    def handle_post(self, user):
        pass
