
import fastapi
import uvicorn
from typing import List
from schemas.user import UserView, UserSubmittal
from services import users

import string, random
from datetime import datetime, timedelta
# import logging

router = fastapi.FastAPI()

# Routers

# GET

@router.get("/user/all", response_model=List[UserView])
async def get_all_users() -> List[UserView]:
    """
    Retrieve all users sorted alphabetically by last name.
    """
    response = await users.get_all_users()
    return response

@router.get("/user/{user_id}", response_model=UserView)
async def get_user(user_id: str):
    """
        Retrieve a user from db using user's id (primary key in db)
    """
    response = await users.get_user(user_id)
    return response


# POST

@router.post("/user/create", response_model=UserView, status_code=201)
async def create_user() -> str:
    """
    Create a new user object and store it at the db.\n
    User related form headings:\n
    id: str\n
    firstName: str\n
    lastName: str\n
    password: str\n
    email: Optional[str]\n
    tel: Optional[str]\n
    birthdate: datetime\n
    nationality: List[str]\n
    sex: str    
    """

    userToBeCreated = UserSubmittal(firstName=get_random_string(4), lastName=get_random_string(4), nickname=get_random_string(6), email=get_random_string(4)+"@mail.com", tel="+3069"+get_random_number(8), password=get_random_number(4), birthdate=datetime.now()-timedelta(days=2), nationality=["GR", "US"], sex="M")
    response = await users.add_user(userToBeCreated)

    return response

# Utillity functions

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def get_random_number(length):
    # choose from digits 0~9
    digits = string.digits
    return ''.join(random.choice(digits) for i in range(length))
    
if __name__ == '__main__':
    uvicorn.run("main:router", port=8000, host='127.0.0.1', reload=True)