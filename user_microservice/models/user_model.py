
from pydantic import BaseModel

class UserModel(BaseModel):
    user_name:str
    user_email:str
    user_password:str
    is_admin:bool=None
    
class UserInDb(BaseModel):
    hashed_password:str
    
class UserModelUpdated(BaseModel):
    user_name:str=None
    user_email:str=None
    user_password:str=None