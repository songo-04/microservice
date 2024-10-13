from fastapi import FastAPI

from router.account_router import account_router

app = FastAPI()

account_router.include_router(account_router)
if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8080)
    