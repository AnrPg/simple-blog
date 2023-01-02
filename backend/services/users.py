
import json
from datetime import datetime
from typing import List
from pydantic import Json
from pydantic_models.user import UserInDB, UserSubmittal, UserView
from infrastructure import users_cache
from uuid import UUID, uuid4

__db = []

# TODO response should be a json with at least two fields; "object" and "status_code"

async def get_user(user_id: UUID) -> UserView | None:
    cached_user = users_cache.get_user(user_id=user_id)
    if cached_user:
        print(f"Retrieved cached user with id: {cached_user.userId}")
        return cached_user
    else:
        retrieved_user =  next((user for user in __db if str(user.userId) == str(user_id)), None)
        if retrieved_user:
            users_cache.add_user(retrieved_user)
            return retrieved_user
        else:
            return None


async def get_all_users() -> List[UserView]:
    if __db:
        __db.sort(key=sort_by_last_name) # [x] Fixed: sort only if __db is NOT EMPTY
    response = __db
    return response

async def add_user(user_to_create: UserSubmittal) -> UserView:
    user_id = uuid4()
    date_created = datetime.now()
    date_last_login = datetime.now()
        
    user_to_create = UserInDB(**user_to_create.dict(), userId=user_id, dateCreated=date_created, dateLastLogin=date_last_login)
    __db.append(user_to_create)

    return user_to_create

async def delete_user(user_id: UUID) -> Json:
    global __db
    users_cache.purge_user(user_id)
    __db = [user for user in __db if str(user.userId) != str(user_id)]
    return json.dumps(f"User with id {user_id} was successfully deleted! :)")

# Utility functions

def sort_by_last_name(item: UserInDB):
    return item.lastName