from fastapi import FastAPI,status,UploadFile,File,Form
from fastapi.middleware.cors import CORSMiddleware
import base64
import cv2
import numpy as np

from config.config import face_collection

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)


def encode_image(image):
    _,buffer = cv2.imencode('.jpg',image)
    return base64.b64encode(buffer).decode('utf-8')


def save_to_mongo(name,face_image):
    person = face_collection.find_one({'name':name})
    if person:
        face_collection.update_one(
            {"name":name},
            {"$addToSet":{"images":face_image}}
        )
    else:
        doc = {
            "name":name,
            "images":[face_image]
        }
        face_collection.insert_one(doc)



@app.post('/api/ai')
async def get(): 
    return {
        "message":"ia service is running"
    }
@app.post('/api/ai/upload')
async def upload_image(name:str=Form(...),file:UploadFile=File(...)):
    contents = await file.read()
    np_array = np.frombuffer(contents,np.uint8)
    image = cv2.imdecode(np_array,cv2.IMREAD_COLOR)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
    
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray,(5,5),0)
    faces = face_cascade.detectMultiScale(blurred,scaleFactor=1.1,minNeighbors=5,minSize=(40,40))

    if len(faces)>0:
        for index,(x,y,w,h) in enumerate(faces):
            face = image[y:y+h,x:x+w]
            encoded_image = encode_image(face)
            save_to_mongo(name,encoded_image)

            
    else:
        return {
            "message":"not face detected"
        }            
    return {"message":"okay"}


if __name__ == "__main__":
    
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=4040)