from fastapi import FastAPI, Response, Request, HTTPException
from fastapi.responses import StreamingResponse
import cv2
import os

app = FastAPI()

# Chemin vers le dossier contenant les fichiers vidéos
MEDIA_FOLDER = "D:/dev/python/microservice/mediaStreamingService/app/videos/"

def get_video_range(file_path, start: int, end: int):
    """
    Renvoie un générateur qui permet de lire un fichier vidéo par morceaux (streaming)
    """
    with open(file_path, "rb") as video:
        video.seek(start)
        while start < end:
            chunk_size = min(1024 * 1024, end - start)  # 1 MB chunks
            data = video.read(chunk_size)
            if not data:
                break
            start += len(data)
            yield data

@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.get("/video_webcam")
async def video_webcam_stream():
    def generate():
        cap = cv2.VideoCapture(0)
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                # Encoder l'image en JPEG
                _, buffer = cv2.imencode('.jpg', frame)
                # Convertir en bytes et yield
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        finally:
            cap.release()

    return StreamingResponse(generate(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/video/{filename}")
async def stream_video(filename: str, request: Request):
    """
    Route pour gérer le streaming vidéo en prenant en charge les requêtes HTTP 'Range'.
    """
    file_path = os.path.join(MEDIA_FOLDER, filename)

    # Vérifier si le fichier existe
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Vidéo non trouvée")

    file_size = os.path.getsize(file_path)
    headers = request.headers
    range_header = headers.get("range")

    # Si la requête contient un header 'Range', extraire la plage demandée
    if range_header:
        range_str = range_header.replace("bytes=", "").split("-")
        start = int(range_str[0])
        end = int(range_str[1]) if range_str[1] else file_size - 1

        # Assurez-vous que les valeurs sont valides
        if start >= file_size or end >= file_size:
            raise HTTPException(status_code=416, detail="Range non satisfiable")

        # Streaming partiel pour la plage demandée
        response = StreamingResponse(get_video_range(file_path, start, end + 1), 
                                     status_code=206)
        response.headers["Content-Range"] = f"bytes {start}-{end}/{file_size}"
        response.headers["Accept-Ranges"] = "bytes"
        response.headers["Content-Length"] = str(end - start + 1)
        response.headers["Content-Type"] = "video/mp4"
    else:
        # Diffusion de la vidéo complète si aucun 'Range' n'est spécifié
        response = StreamingResponse(get_video_range(file_path, 0, file_size), 
                                     media_type="video/mp4")
        response.headers["Content-Length"] = str(file_size)

    return response
