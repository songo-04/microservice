FROM python:3.12-slim

WORKDIR /app
 
COPY requirement.txt /app

RUN pip install -r requirement.txt

COPY ./app /app/

CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000","--reload"]
