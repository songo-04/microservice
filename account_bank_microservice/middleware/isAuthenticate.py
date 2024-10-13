from fastapi import Request,HTTPException,status
from dotenv import load_dotenv
import os
import jwt

load_dotenv()

async def is_authenticate(request:Request):
    try:
        token = request._cookies.get('access_token')
        if not token:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail='token not found'
            )
        user_info = jwt.decode(token,os.getenv('SECRET_KEY'),algorithms=[os.getenv('ALGORITHM')])
        userId = user_info.get('userId')
        if not userId:
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail= 'invalid token'
            )
        return user_info
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= 'invalid token'
        )