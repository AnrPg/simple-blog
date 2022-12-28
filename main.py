
import fastapi
import uvicorn
from typing import List
from schemas.user import UserView

router = fastapi.FastAPI()

@router.get("/user/all", response_model=List[UserView])
def read_items() -> List[UserView]:
    """
    Retrieve user.
    """

    # response = [UserView(id='1', firstName='Anr', lastName='Pg', email='anr@email.com'), UserView(id='2', firstName='Maria', lastName='Annou', email='ma@email.com')]
    return response

@router.post("/user/create")
def create_user() -> str:
    """
    Create a new user object and store it at the db.
    User related form headings:
    !!!!!!!!!!!!!!    
    """
    

if __name__ == '__main__':
    uvicorn.run(router, port=8000, host='127.0.0.1')