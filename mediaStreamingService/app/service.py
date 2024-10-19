from fastapi import FastAPI, Response, Request, HTTPException, Depends, status
from fastapi.responses import StreamingResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import cv2
import os
from typing import Optional
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from urllib.parse import unquote
import uvicorn

app = FastAPI()

# Configuration pour servir les fichiers statiques et les templates
app.mount("/templates", StaticFiles(directory="templates"), name="templates")
templates = Jinja2Templates(directory="templates")

# Chemin vers le dossier contenant les fichiers vidéos
MEDIA_FOLDER = "D:/media/FILM/"

security = HTTPBasic()

users = {"admin": "admin", "user": "admin"}


class LoginData(BaseModel):
    username: str
    password: str


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    if username not in users or users[username] != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects",
            headers={"WWW-Authenticate": "Basic"},
        )
    return username


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_video_range(file_path, start: int, end: int):
    with open(file_path, "rb") as video:
        video.seek(start)
        while start < end:
            chunk_size = min(1024 * 1024, end - start)  # 1 MB chunks
            data = video.read(chunk_size)
            if not data:
                break
            start += len(data)
            yield data


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(login_data: LoginData):
    if (
        login_data.username in users
        and users[login_data.username] == login_data.password
    ):
        return {"success": True}
    raise HTTPException(status_code=400, detail="Identifiants incorrects")


@app.get("/home", response_class=HTMLResponse)
async def home(request: Request, username: str = Depends(get_current_username)):
    video_files = [
        f for f in os.listdir(MEDIA_FOLDER) if f.endswith((".mp4", ".avi", ".mov"))
    ]
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "video_files": video_files, "username": username},
    )


@app.get("/api/videos")
async def list_videos():
    video_files = [
        f for f in os.listdir(MEDIA_FOLDER) if f.endswith((".mp4", ".avi", ".mov"))
    ]
    return {"videos": video_files}


@app.get("/api/video/{filename:path}")
async def stream_video(filename: str, username: str = Depends(get_current_username)):
    # Décodez le nom du fichier
    filename = unquote(filename)
    file_path = os.path.join(MEDIA_FOLDER, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Vidéo non trouvée")

    file_size = os.path.getsize(file_path)
    headers = Request.headers
    range_header = headers.get("range")

    if range_header:
        range_str = range_header.replace("bytes=", "").split("-")
        start = int(range_str[0])
        end = int(range_str[1]) if range_str[1] else file_size - 1

        if start >= file_size or end >= file_size:
            raise HTTPException(status_code=416, detail="Range non satisfiable")

        response = StreamingResponse(
            get_video_range(file_path, start, end + 1), status_code=206
        )
        response.headers["Content-Range"] = f"bytes {start}-{end}/{file_size}"
        response.headers["Accept-Ranges"] = "bytes"
        response.headers["Content-Length"] = str(end - start + 1)
        response.headers["Content-Type"] = "video/mp4"
    else:
        response = StreamingResponse(
            get_video_range(file_path, 0, file_size), media_type="video/mp4"
        )
        response.headers["Content-Length"] = str(file_size)

    return response


if __name__ == "__main__":
    uvicorn.run(
        "app.service:app",
        host="0.0.0.0",
        port=5000,
        ssl_keyfile="path/to/key.pem",
        ssl_certfile="path/to/cert.pem",
    )
