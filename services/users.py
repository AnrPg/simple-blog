

import shortuuid
from schemas.user import UserInDB, UserSubmittal, UserView
from datetime import datetime
from random import seed, randint
from typing import List

__cache = []

def sort_by_last_name(item: UserInDB):
    return item.lastName


async def get_all_users() -> List[UserView]:
    __cache.sort(key=sort_by_last_name)
    response = __cache
    return response

async def add_user(user_to_create: UserSubmittal) -> UserView:
    user_id = str(shortuuid.uuid())
    date_created = datetime.now()
    date_last_login = datetime.now()

    user_to_create = UserInDB(**user_to_create.dict(), userId=user_id, dateCreated=date_created, dateLastLogin=date_last_login)
    __cache.append(user_to_create)

    return user_to_create