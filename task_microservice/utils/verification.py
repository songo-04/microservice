from fastapi import HTTPException,status

def is_exist(x):
    if not x:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='not found'
        )
def is_empty(x):
    if len(x) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='empty !!'
        )
def is_authorize(db_id,token_id):
    if db_id != token_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='access denied !'
        )