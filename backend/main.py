
import fastapi
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
from typing import List
from pydantic import Json
from pydantic_models.user import UserView, UserSubmittal
from services import users
from uuid import UUID

import string, random
from datetime import datetime, timedelta
# import logging

# TODO check if services' responses are sound and return error message elsehow

router = fastapi.FastAPI()

origins = [
    "http://localhost:3000",
    "https://localhost:3000"
]

router.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Routers

# GET

@router.get("/api/user/all", response_model=List[UserView])
async def get_all_users() -> List[UserView]:
    """
    Retrieve all users sorted alphabetically by last name.
    """
    for i in [1]:
        userToBeCreated = create_sample_user()
        await users.add_user(userToBeCreated)

    response = await users.get_all_users()
    print(response)
    return response

@router.get("/api/user/{user_id}", response_model=UserView)
async def get_user(user_id: UUID):
    """
        Retrieve a user from db using user's id (primary key in db)
    """
    response = await users.get_user(user_id)
    return response


# POST

@router.post("/api/user/create", response_model=UserView, status_code=201)
async def create_user() -> UserView:
    """
    Create a new user object and store it at the db.\n
    User related form headings:\n
    id: uuid4\n
    firstName: str\n
    lastName: str\n
    password: str\n
    email: Optional[str]\n
    tel: Optional[str]\n
    birthdate: datetime\n
    nationality: List[str]\n
    sex: str    
    """

    # TODO create front-end form to supply this endpoint with the data required to create user
    userToBeCreated = create_sample_user()
    response = await users.add_user(userToBeCreated)

    return response # json.dumps(response.dict())

    # DELETE

@router.delete("/api/user/{user_id}", status_code=204)
async def delete_user(user_id: UUID) -> Json:
    response = await users.delete_user(user_id) # TODO use status code from response to assess success of request
    # if not response or response.status_code != 204: 
    #     response = {
    #         'error_message':'empty response from server',
    #         'status_code': 500
    #     }
    #     return json.load(response)
    # else:
    return json.dumps(f"Successfully deleted user with id: {user_id} ! :)")

# Utillity functions

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def get_random_number(length):
    # choose from digits 0~9
    digits = string.digits
    return ''.join(random.choice(digits) for i in range(length))

def create_sample_user() -> UserSubmittal:
    return UserSubmittal(firstName=get_random_string(4), lastName=get_random_string(4), nickname=get_random_string(6), email=get_random_string(4)+"@mail.com", tel="+3069"+get_random_number(8), password=get_random_number(4), birthdate=datetime.now()-timedelta(days=2), nationality=["GR", "US"], gender='Male')
    
    
if __name__ == '__main__':
    uvicorn.run("main:router", port=8000, host='127.0.0.1', reload=True)