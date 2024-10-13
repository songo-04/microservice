
from fastapi import APIRouter,Request,Response,HTTPException,status,Depends
from passlib.context import CryptContext
from datetime import datetime, timedelta
from dotenv import load_dotenv
from bson import ObjectId
from pymongo.errors import PyMongoError

import jwt
import os


from models.user_model import UserModel,UserModelUpdated
from models.profile_model import ProfileModel
from config.config import user_collection
from config.config import profile_collection
from serialize.user_serialize import Decode_user,Decode_users,Decode_user_admin
from utils.is_auth import is_authenticate

load_dotenv()

user_route = APIRouter(
    prefix='/api/user'
)

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

#hash password
def get_password_hash(password):
    return pwd_context.hash(password)
#verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Creation de token JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + timedelta(minutes=15)
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    

#create user
@user_route.post('/register')
async def create_user(data:UserModel):
    is_user_exist = user_collection.find_one({"user_email":str(data.user_email)})
    if(is_user_exist):
        raise HTTPException(
            status_code=status.HTTP_226_IM_USED,detail='already exciting'
        )
    new_user= UserModel(
        user_name=data.user_name,
        user_email=data.user_email,
        user_password=get_password_hash(data.user_password),
        is_admin=False
        )
    new_user=dict(new_user)
    try:
        insert_user = user_collection.insert_one(new_user)
        if not insert_user.acknowledged:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='failed to insert user'
            )
        user = user_collection.find_one({"user_email":data.user_email})
        user = Decode_user_admin(user)
        new_profile = ProfileModel(
            name=' ',
            surname=' ',
            email= data.user_email,
            address= ' ',
            userId= user['_id']
        )
        new_profile = dict(new_profile)
        insert_profile = profile_collection.insert_one(new_profile)
        if not insert_profile.acknowledged:
            await user_collection.find_one_and_delete({'_id':user['_id']})
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='failed to insert profile'
            )
    except PyMongoError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"failed {str(e)}"
        )
    

#login
@user_route.post('/login')
async def login(data_form:UserModel,response:Response):
    is_user_exist = user_collection.find_one({"user_email":data_form.user_email})
    if not is_user_exist or not verify_password(data_form.user_password,is_user_exist['user_password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='access denied'
        )
    access_token_expire = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token  = create_access_token(
        data={"userId":str(is_user_exist['_id']),"sub":is_user_exist['user_name']},
        expires_delta=access_token_expire
        )
    response.set_cookie(key="access_token",value=access_token,httponly=True)
    return {
        "message":"login successfully"
    }

@user_route.get('/me')
async def current_user(is_auth:dict=Depends(is_authenticate)):
    userId=is_auth['userId']
    user = user_collection.find_one({"_id":ObjectId(userId)})
    if(not user):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user empty'
        )
    user = Decode_user(user)
    return user

#update
@user_route.patch('/update')
async def update_current_user(data_form:UserModelUpdated,is_auth: dict=Depends(is_authenticate)):
    userId = is_auth['userId']
    req = dict(data_form.model_dump(exclude_unset=True))
    user_collection.find_one_and_update({"_id":ObjectId(userId)},{"$set":req})
    return {
        "message":"user id {_id} updated",
        "status":status.HTTP_200_OK
    }

#delete
@user_route.delete('/delete')
async def delete_current_user(res:Response,is_auth: dict=Depends(is_authenticate)):
    userId = is_auth['userId']
    user_collection.find_one_and_delete({'_id':ObjectId(userId)})
    res.delete_cookie(key='access_token')
    return {
        "message":"user deleted"
    }

@user_route.get('/logout')
async def logout(res:Response,is_auth: dict=Depends(is_authenticate)):
    res.delete_cookie(key='access_token')
    return {
        "message":"log out"
    }