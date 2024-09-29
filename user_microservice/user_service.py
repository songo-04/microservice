from fastapi import FastAPI

from routes.user_route import user_route
from routes.profile_route import profile_route

app = FastAPI()

app.include_router(user_route)
app.include_router(profile_route)

@app.get('/api/user')
async def get(): 
    return {
        "message":"user service is running"
    }
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=5000)