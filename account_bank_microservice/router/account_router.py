from fastapi import APIRouter,HTTPException,Request,Response,Depends,status

from middleware.isAuthenticate import is_authenticate

account_router = APIRouter(
    prefix='/api/account'
)

@account_router.get('/')
async def welcome():
    # userId = is_auth['userId']
    # if not userId:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail='not authorized'
    #     )
    
    return {
        "message":"welcome to your bank account"    
    }
@account_router.post('/create/')
async def create_account(data:dict):
    pass

@account_router.get('/find')
async def get_account():
    pass

