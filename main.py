
import fastapi
import uvicorn
import shortuuid
from typing import List

from schemas.user import UserView, UserDetailed
from services import users

from datetime import datetime, timedelta

router = fastapi.FastAPI()

@router.get("/user/all", response_model=List[UserView])
def read_items() -> List[UserView]:
    """
    Retrieve user.
    """
    response = [users.get_user()]
    # response = [UserView(id='1', firstName='Anr', lastName='Pg', email='anr@email.com'), UserView(id='2', firstName='Maria', lastName='Annou', email='ma@email.com')]
    return response

@router.post("/user/create")
def create_user() -> str:
    """
    Create a new user object and store it at the db.
    User related form headings:
    id: str
    firstName: str
    lastName: str
    password: str
    email: Optional[str]
    tel: Optional[str]
    birthdate: datetime
    nationality: List[str]
    sex: str    
    """

    userToBeCreated = UserDetailed(id=shortuuid.uuid().__str__(), firstName="troll", lastName="tril", email="", tel="", password="", birthdate=datetime.now()-timedelta(days=2), nationality=[""], sex="", dateCreated=datetime.now(), dateLastLogin=datetime.now()+timedelta(days=1))
    try:
        response = users.add_user(userToBeCreated)
    except:
        pass

    return response

if __name__ == '__main__':
    uvicorn.run(router, port=8000, host='127.0.0.1')