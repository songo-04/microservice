from fastapi import APIRouter,HTTPException,Request,Response,Depends

account_router = APIRouter('/api/account')

@account_router.get('/')
async def welcome():
    pass

@account_router.post('/create/')
async def create_account(data:dict):
    pass

@account_router.get('/find')
async def get_account():
    pass

