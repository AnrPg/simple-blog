from uuid import UUID, uuid4
from typing import Optional, List, TypeVar, Literal
from datetime import datetime
from pydantic import BaseModel, Field, constr, validator, root_validator #SecretStr
from pydantic_models.my_exceptions import MalformedFullName, MissingIdentifier, MalformedTelephone, MalformedDate
from email_validator import validate_email, EmailNotValidError
import re

Id = TypeVar("Id", UUID, int, str)
class BaseUser(BaseModel):    
    firstName: Optional[str]
    lastName: Optional[str]
    nickname: Optional[str]
    email: Optional[str]
    tel: Optional[str]

    @validator('email')
    def check_email(cls, submitted_email):
        return validate_email(email=submitted_email, check_deliverability=True).email

    @validator('tel')
    def check_tel_format(cls, submitted_tel, values):

        if not 'tel' in values:
            return submitted_tel # NOTE I don't know when is this validator executed and when values arg is available, but as I've seen so far, the time we need it, it doesn't contain 'tel' in values, so this check is uneeded
        elif not re.match(r"^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$", submitted_tel):
            raise MalformedTelephone("Malformed telephone number", status_code=602)
        else:
            return submitted_tel
        
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
    password: constr(min_length=4) #constr(regex=r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[?!@$%^&*-#\(\)\{\}\_\=\+]).{8,}$")
    birthdate: str
    nationality: List[constr(min_length=2, max_length=2)]
    gender: Literal['Male', 'Female', 'Non-binary', 'Prefer not to say', 'male', 'female', 'non-binary', 'prefer not to say', 'MALE', 'FEMALE', 'NON-BINARY', 'PREFER NOT TO SAY', 'M', 'F', 'N', 'U', 'm', 'f', 'n', 'u']
    
    @validator('birthdate')
    def check_birthday_format(cls, date_value):
        parsed_date_dict = parse_date(date_string=date_value)
        
        if is_valid_date(int(parsed_date_dict["year"]), int(parsed_date_dict["month"]), int(parsed_date_dict["day"])):
            return date_value
        else:
            raise MalformedDate(error_message="Malformed date of birth", status_code=603)


class UserInDB(UserSubmittal):
    userId: Id = Field(default_factory = uuid4())
    dateCreated: datetime = Field(default_factory = datetime.now())
    dateLastLogin: datetime = Field(default_factory = datetime.now())
    
class UserView(BaseUser):
    userId: Id = Field(default_factory = uuid4())

# UTILITIES FUNCTIONS

def is_valid_date(year: int, month: int, day: int, hours: int | None = 0, minutes: int | None  = 0, seconds: int | None  = 0, milliseconds: int | None  = 0, location: str | None  = ""):
    day_count_for_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if year%4==0 and (year%100 != 0 or year%400==0):
        day_count_for_month[2] = 29
    return (1 <= month <= 12 and 1 <= day <= day_count_for_month[month] and 0 <= hours <= 24 and 0 <= minutes <= 59 and 0 <= seconds <= 59)

def parse_date(date_string: str) -> dict:
    """
        Input date should be in the format YYYY[]MM[]DD hh:mm:ss.m location (where [] means any separator e.g. -\/.: ) to be successfully parsed
    """
    match = parse_various_format_dates(date_string)

    if not match:
        raise MalformedDate(error_message="Malformed date of birth.\n\
                                        Date formats accepted:\n\
                                        YYYY[]MM[]DD hh:mm:ss.m location\n\
                                        YYYY[]DD[]MM hh:mm:ss.m location\n\
                                        MM[]DD[]YYYY hh:mm:ss.m location\n\
                                        DD[]MM[]YYYY hh:mm:ss.m location\n\
                                        Couldn't parse input", status_code=604)
    else:
        return {
            "year" : match.group('year'),
            "month" : match.group('month'),
            "day" : match.group('day'),
            "hours" : match.group('hours'),
            "minutes" : match.group('minutes'),
            "seconds" : match.group('seconds'),
            "milliseconds" : match.group('milliseconds'),
            "location" : match.group('location')
        }

def parse_various_format_dates(date_string: str) -> (re.Match[str] | None):
    """
        Input date should be in the format YYYY[]DD[]MM hh:mm:ss.m location (where [] means any separator e.g. -\/.: ) to be successfully parsed
    """
    # YYYY[]MM[]DD hh:mm:ss.m location
    pattern = re.compile("^(?P<year>\d{4})[-/\\\s._](?P<month>(0?[1-9]|1[0-2]))[-/\\\w._](?P<day>(0?[1-9]|[12][0-9]|3[01]))(\s(?P<hours>(00|[0-9]|1[0-9]|2[0-3])):(?P<minutes>([0-9]|[0-5][0-9])):(?P<seconds>([0-9]|[0-5][0-9]))(?P<milliseconds>(?:\.\d+)?)(?P<location>(?: \S+\/\S+)?))?$")    
    match = pattern.match(date_string)

    if match:
        return match
    else:
        # YYYY[]DD[]MM hh:mm:ss.m location
        pattern = re.compile("^(?P<year>\d{4})[-/\\\s._](?P<day>(0?[1-9]|[12][0-9]|3[01]))[-/\\\w._](?P<month>(0?[1-9]|1[0-2]))(\s(?P<hours>(00|[0-9]|1[0-9]|2[0-3])):(?P<minutes>([0-9]|[0-5][0-9])):(?P<seconds>([0-9]|[0-5][0-9]))(?P<milliseconds>(?:\.\d+)?)(?P<location>(?: \S+\/\S+)?))?$")
        match = pattern.match(date_string)

        if match:
            return match
        else:
            # DD[]MM[]YYYY hh:mm:ss.m location
            pattern = re.compile("^(?P<day>(0?[1-9]|[12][0-9]|3[01]))[-/\\\s._](?P<month>(0?[1-9]|1[0-2]))[-/\\\w._](?P<year>\d{4})(\s(?P<hours>(00|[0-9]|1[0-9]|2[0-3])):(?P<minutes>([0-9]|[0-5][0-9])):(?P<seconds>([0-9]|[0-5][0-9]))(?P<milliseconds>(?:\.\d+)?)(?P<location>(?: \S+\/\S+)?))?$")
            match = pattern.match(date_string)

            if match:
                return match
            else:
                # MM[]DD[]YYYY hh:mm:ss.m location
                pattern = re.compile("^(?P<month>(0?[1-9]|1[0-2]))[-/\\\s._](?P<day>(0?[1-9]|[12][0-9]|3[01]))[-/\\\w._](?P<year>\d{4})(\s(?P<hours>(00|[0-9]|1[0-9]|2[0-3])):(?P<minutes>([0-9]|[0-5][0-9])):(?P<seconds>([0-9]|[0-5][0-9]))(?P<milliseconds>(?:\.\d+)?)(?P<location>(?: \S+\/\S+)?))?$")
                match = pattern.match(date_string)

                if match:
                    return match
                else:
                    return None