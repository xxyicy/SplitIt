from google.appengine.ext import ndb

from handlers.base_handlers import BaseAction


class DeleteGroupAction(BaseAction):
  def handle_post(self, user):
      group_key = ndb.Key(urlsafe=self.request.get('group_to_delete_key'))
      group_key.delete();
      self.redirect("/")  
    
    
class DeleteEventAction(BaseAction):
    def handle_post(self, user):
<<<<<<< HEAD
        # TODO: delete from db and get group_key     
        group_key = ""
=======
        event_key = ndb.Key(urlsafe=self.request.get("event_to_delete_key"))
        event = event_key.get()
        group_key = event.group_key
        group =  ndb.Key(urlsafe=group_key).get()
        
        group.events.remove(event_key)
        group.put()
        event_key.delete()
>>>>>>> master
        self.redirect("/events?group_key=" + group_key)
