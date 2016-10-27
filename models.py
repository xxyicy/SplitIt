from google.appengine.ext import ndb


class User(ndb.Model):
    id = ndb.StringProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty()
    access_token = ndb.StringProperty(required=True)
    username = ndb.StringProperty()
    avatarUrl = ndb.StringProperty()
    phoneNumber = ndb.StringProperty()

class Event(ndb.Model):
    eventName = ndb.StringProperty()
    eventDescript = ndb.StringProperty()
    members = ndb.KeyProperty(kind=User,repeated=True)
    expenses = ndb.IntegerProperty(repeated=True)
    
class Group(ndb.Model):
    groupName = ndb.StringProperty()
    groupDescript = ndb.StringProperty()
    members = ndb.KeyProperty(kind=User,repeated=True)
    events = ndb.KeyProperty(kind=Event,repeated=True)
    expenses = ndb.IntegerProperty(repeated=True)
    