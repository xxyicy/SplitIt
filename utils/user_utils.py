from google.appengine.ext import ndb
from models import User


def get_parent_key_from_facebookID(facebookID):
  return ndb.Key("Entity", facebookID.lower())
  
def get_user_by_facebookID(facebookID):
    return User.get_by_id(facebookID, parent=get_parent_key_from_facebookID(facebookID))  