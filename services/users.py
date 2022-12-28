

from schemas.user import UserDetailed

__cache = []

def get_user() -> UserDetailed:
    return  __cache[0] #f"{{\"response\":\"Success!\", \"user id\":\"{user_to_create.id}\"}}" 

def add_user(user_to_create: UserDetailed) -> str:
    __cache.append(user_to_create)
    return f"{{\"response\":\"Success!\", \"user id\":\"{user_to_create.id}\"}}"