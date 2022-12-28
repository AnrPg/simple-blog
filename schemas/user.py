from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class BaseUser(BaseModel):
    id: str
    firstName: str
    lastName: str
    email: Optional[str]
    tel: Optional[str]
    

class UserDetailed(BaseUser):
    password: str
    birthdate: datetime
    nationality: List[str]
    sex: str
    dateCreated: datetime
    dateLastLogin: datetime

class UserView(BaseUser):
    age: Optional[int]
