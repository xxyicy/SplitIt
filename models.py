from google.appengine.ext import ndb

class User(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    name = ndb.StringProperty()
    email = ndb.StringProperty(default="")
    access_token = ndb.StringProperty(required=True)
    nickname = ndb.StringProperty(default="")
    avatarUrl = ndb.StringProperty(default="")
    phoneNumber = ndb.StringProperty(default="")

class Friend(ndb.Model):
    nickname = ndb.StringProperty(default="")
    email = ndb.StringProperty(default="")
    phoneNumber = ndb.StringProperty(default="")

class Event(ndb.Model):
    eventName = ndb.StringProperty()
    eventDescription = ndb.StringProperty()
    members = ndb.KeyProperty(kind=Friend,repeated=True)
    expenses = ndb.IntegerProperty()
    
class Group(ndb.Model):
    groupName = ndb.StringProperty()
    groupDescription = ndb.StringProperty()
    members = ndb.KeyProperty(kind=Friend,repeated=True)
    events = ndb.KeyProperty(kind=Event,repeated=True)
    expenses = ndb.IntegerProperty(repeated=True)
    

    
    