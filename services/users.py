

import shortuuid
from datetime import datetime
from typing import List
from schemas.user import UserInDB, UserSubmittal, UserView
from infrastructure import users_cache

__db = []

async def get_user(user_id: str) -> UserView | None:
    cached_user = users_cache.get_user(user_id=user_id)
    if cached_user:
        print(f"Retrieved cached user with id: {cached_user.userId}")
        return cached_user
    else:
        retrieved_user =  next((user for user in __db if user.userId == user_id), None)
        if retrieved_user:
            users_cache.add_user(retrieved_user)
            return retrieved_user
        else:
            return None


async def get_all_users() -> List[UserView]:
    __db.sort(key=sort_by_last_name)
    response = __db
    return response

async def add_user(user_to_create: UserSubmittal) -> UserView:
    user_id = str(shortuuid.uuid())
    date_created = datetime.now()
    date_last_login = datetime.now()
    
    user_to_create = UserInDB(**user_to_create.dict(), userId=user_id, dateCreated=date_created, dateLastLogin=date_last_login)
    __db.append(user_to_create)

    return user_to_create

# Utility functions

def sort_by_last_name(item: UserInDB):
    return item.lastName