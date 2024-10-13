
from pydantic import BaseModel

class ProfileModel(BaseModel):
    name:str=None
    surname:str=None
    email:str=None
    address:str
    userId:str=None

class ProfileModelUpdate(BaseModel):
    name:str=None
    surname:str=None
    address:str=None