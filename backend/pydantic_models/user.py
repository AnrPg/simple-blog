from uuid import UUID, uuid4
from typing import Optional, List, TypeVar, Literal
from datetime import datetime
from pydantic import BaseModel, EmailStr, PastDate, Field, constr, root_validator #SecretStr
from pydantic_models.my_exceptions import MalformedFullName, MissingIdentifier

Id = TypeVar("Id", UUID, int, str)
class BaseUser(BaseModel):    
    firstName: Optional[str]
    lastName: Optional[str]
    nickname: Optional[str]
    email: Optional[EmailStr]
    tel: Optional[constr(regex=r"^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$")]

    @root_validator(pre=True)
    def check_name_has_both_fields(cls, values):
        if (('firstName' in values and 'lastName' not in values) or ('firstName' not in values and 'lastName' in values)):
            raise MalformedFullName(error_message="You have to specify both first name AND last name (or no name at all)", firstname_present=('firstName' in values), lastname_present=('lastName' in values), status_code=601) # status codes are set by me to spot immediately at which point of code the exception was raised
        else:
            return values

    @root_validator(pre=True)
    def check_some_identifier_is_given(cls, values):
        if (('firstName' not in values or 'lastName' not in values) and ('nickname' not in values) and ('email' not in values) and ('tel' not in values)):
            raise MissingIdentifier(error_message="You should specify one of the following: email , tel, nickname, full name (first and last name)", status_code=601) # status codes are set by me to spot immediately at which point of code the exception was raised
        else:
            return values
    

class UserSubmittal(BaseUser):    
    password: constr(min_length=4) | None #constr(regex=r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[?!@$%^&*-#\(\)\{\}\_\=\+]).{8,}$")
    birthdate: PastDate | str
    nationality: List[constr(min_length=2, max_length=2)] | None
    gender: Literal['Male', 'Female', 'Non-binary', 'Prefer not to say'] | None

class UserInDB(UserSubmittal):
    userId: Id = Field(default_factory = uuid4())
    dateCreated: datetime = Field(default_factory = datetime.now())
    dateLastLogin: datetime = Field(default_factory = datetime.now())
    
class UserView(BaseUser):
    userId: Id = Field(default_factory = uuid4())