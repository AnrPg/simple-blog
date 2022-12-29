

from schemas.user import UserInDB, UserSubmittal, UserView
import shortuuid
from datetime import datetime
from random import randint

__cache = []

def get_user() -> UserInDB:
    random.seed(datetime.now())
    return  __cache[randint(0, len(__cache))] #f"{{\"response\":\"Success!\", \"user id\":\"{user_to_create.id}\"}}" 

def add_user(user_to_create: UserSubmittal) -> UserView:
    user_id = str(shortuuid.uuid())
    date_created = datetime.now()
    date_last_login = datetime.now()

    user_to_create = UserInDB(**user_to_create.dict(), userId=user_id, dateCreated=date_created, dateLastLogin=date_last_login)
    __cache.append(user_to_create)

    return user_to_create