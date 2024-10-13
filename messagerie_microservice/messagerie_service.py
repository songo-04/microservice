from fastapi import FastAPI # type: ignore

from routes.message_private_router import message_private_router
app = FastAPI()

app.include_router(message_private_router)

@app.get('/api/message')
async def get(): 
    return {
        "message":"messagerie service is running"
    }
    
if __name__ == "__main__":
    
    import uvicorn # type: ignore
    uvicorn.run(app,host="0.0.0.0",port=5050)