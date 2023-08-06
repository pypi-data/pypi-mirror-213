from enum import Enum

from pydantic import BaseModel


class ResponseMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATH = "PATCH"
    DELETE = "DELETE"


class CoreCommand(Enum):
    CREATE = "CORE||CREATE_OBJECT|"
    UPDATE = "CORE||UPDATE_OBJECT|"
    DELETE = "CORE||DELETE_OBJECT|"


class ObjectType(Enum):
    PERSON = "<PERSON>"
    DEPARTMENT = "<DEPARTMENT>"


class AutarizationInfo(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class IntellectConfigDto(BaseModel):
    intellect_host: str
    intellect_port: int
    host_user: str
    host_password: str
    token_expires: int  # seconds
    access_level: int
    access_department_id: int  # for temp pass


class IntellectVisitDto:
    class Create(BaseModel):
        objid: int
        name: str | None  # second_name
        surname: str | None  # first_name
        patronymic: str | None  # middle_name
        parent_id: int  # department_id
        email: str | None  # email
        phone: str | None  # phone
        visit_birthplace: str | None  # place_of_birth
        visit_reg: str | None  # registration
        facility_code: str | None
        level_id: int | None  # access_level
        visit_purpose: str | None
        card: str | None

    class Update(BaseModel):
        objid: int
        name: str | None  # second_name
        surname: str | None  # first_name
        patronymic: str | None  # middle_name
        parent_id: int | None  # department_id
        email: str | None  # email
        phone: str | None  # phone
        visit_birthplace: str | None  # place_of_birth
        visit_reg: str | None  # registration
        facility_code: str | None
        level_id: int | None  # access_level
        visit_purpose: str | None
        card: str | None


class IntellectDepartmentDto:
    class Create(BaseModel):
        objid: str
        name: str  # unique_name
        schedule_id: str | None
        level_id: str | None
        region_id: str | None
        external_id: str | None
        owner_id: str | None

    class Update(BaseModel):
        schedule_id: str | None
        objid: str | None
        name: str | None
        level_id: str | None
        region_id: str | None
        external_id: str | None
        owner_id: str | None
