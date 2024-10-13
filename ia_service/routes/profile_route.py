from fastapi import APIRouter, Response ,status,Depends,HTTPException
from bson import ObjectId

from utils.is_auth import is_authenticate
from models.profile_model import ProfileModel,ProfileModelUpdate
from config.config import profile_collection
from serialize.profile_serialize import Decode_profile,Decode_profiles

profile_route = APIRouter(
    prefix='/api/user/profile'
)

#get profile
@profile_route.get('/me')
async def get_profile(is_auth:dict=Depends(is_authenticate)):
    userId = is_auth['userId']
    profile = profile_collection.find_one({'userId':userId})
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='profile not found'
        )
    return Decode_profile(profile)

#put
@profile_route.patch('/update')
async def update_profile(data_form: ProfileModelUpdate,is_auth: dict=Depends(is_authenticate)):
    userId = is_auth['userId']
    req = dict(data_form.model_dump(exclude_unset=True))
    profile_collection.find_one_and_update({"userId":userId},{"$set":req})
    return {
        "message":"profile updated !!!",
        "status":status.HTTP_200_OK
    }