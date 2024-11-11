from fastapi import FastAPI

from routes.simple_task_route import simple_task_route
app = FastAPI()


app.include_router(simple_task_route)
@app.get('/api/task')
async def task_welcome():
    return {
        "message":"task service is running"
    }

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,port=8002)
