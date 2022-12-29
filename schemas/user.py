from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class BaseUser(BaseModel):    
    firstName: Optional[str]
    lastName: Optional[str]
    nickname: Optional[str]
    email: Optional[str]
    tel: Optional[str]
    

class UserSubmittal(BaseUser):    
    password: str
    birthdate: datetime
    nationality: List[str]
    sex: str

class UserInDB(UserSubmittal):
    userId: str
    dateCreated: datetime
    dateLastLogin: datetime

class UserView(BaseUser):
    pass
