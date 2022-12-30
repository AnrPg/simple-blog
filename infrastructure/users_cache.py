from datetime import datetime, timedelta
from typing import Optional
from pydantic import StrictBool
from pydantic_models.user import UserView, UserInDB

__cache = {}
lifetime_in_hours = 1.5

def get_user(user_id: str) -> Optional[UserView]:
    """
    Fetches a user object from cache iff this object is not outdated.
    Else, returns None (so the cached version of the object -if ever existed- is outdated and thus, unneeded)
    """
    data: dict = __cache.get(user_id)
    if not data:
        return None
    
    last = data["time"]
    dt = datetime.now() - last
    if dt / timedelta(minutes=60) < lifetime_in_hours:
        return data["value"]
    else:
        del __cache[user_id]
        return None 

def add_user(user_to_cache: UserInDB):
    """
    Stores a user object to the cache (as a dict) along with information about the time this storing was done
    so that we can keep track of how recent our items are in the cache
    """
    data = {
        "time"  : datetime.now(),
        "value" : user_to_cache
    }

    __cache[user_to_cache.userId] = data
    __clean_out_of_date()

# Utility functions

def is_out_of_date(data: dict) -> StrictBool:
    """
    Input dictionary must be of the form:\n
    { "time" : datetime_of_last_set , "value" : object_to_be_cached }
    \n
    Returns True if input is outdated according to the pre-set lifetime_in_hours,
    else, returns False
    """

    last = data["time"]
    dt = datetime.now() - last
    if dt / timedelta(minutes=60) > lifetime_in_hours:
        return True
    else:
        return False

def __clean_out_of_date():
    """
    Removes items in __cache that are outdated (in relevance with lifetime_in_hours)
    """
    (data for data in __cache if not is_out_of_date(data))