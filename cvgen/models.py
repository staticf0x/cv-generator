from typing import List

from pydantic import BaseModel, EmailStr, HttpUrl


class Config(BaseModel):
    key: str
    name: str
    lang: str
    jobs: List[str]
    address: bool
    education: List[str]
    intro: bool
    skills: str
    disabled: bool = False


class Contact(BaseModel):
    name: str
    phone: str
    email: EmailStr
    address: str
    github: HttpUrl
