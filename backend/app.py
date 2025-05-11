from fastapi import FastAPI, HTTPException, status, File, UploadFile, APIRouter
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from repositories.DataRepository import DataRepository
import socketio
from models.models import foto, tekst, DTOFotoToDB, DTOTekst, DTOFotoToFolder
import os
import cloudinary
import cloudinary.uploader

ENDPOINT = "/api/v1/"

cloudinary.config(cloud_name = os.getenv("CL_NAME"), api_key = os.getenv("CL_API"), api_secret = os.getenv("CL_SECRET"))

app = FastAPI(title="In memory of Tiebe", debug=True, description="In memory of Tiebe", version="1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)

sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi', logger=True)
sio_app = socketio.ASGIApp(sio, app)

async def send_fotos_en_teksten_via_sio():
    data_teksten = DataRepository.read_tekst()
    if data_teksten is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="teksten niet gevonden")
    
    data_fotos = DataRepository.read_foto_pad()
    if data_fotos is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="fotos niet gevonden")

    await sio.emit("B2F_new_content_added", {'status': 'new contend is added', 'teksten': data_teksten, 'fotos': data_fotos})

@sio.event
async def connect(sid, environ):
    print(f'[Socket.IO] Client geconnecteerd: {sid}')
    data_teksten = DataRepository.read_tekst()
    if data_teksten is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="teksten niet gevonden")
    
    data_fotos = DataRepository.read_foto_pad()
    if data_fotos is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="fotos niet gevonden")
    await sio.emit("B2F_connected", {'status': 'new contend is added', 'teksten': data_teksten, 'fotos': data_fotos}, to=sid)

@app.get(ENDPOINT + 'foto/', response_model=list[foto], summary="Get alle foto's")
async def fotos():
    data = DataRepository.read_foto_pad()
    print(data)
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="fotos niet gevonden")
    return data

@app.get(ENDPOINT + 'tekst/', response_model=list[tekst], summary="Get alle teksten")
async def teksten():
    data = DataRepository.read_tekst()
    print(data)
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="teksten niet gevonden")
    return data

# @app.post(ENDPOINT + 'fotoToFolder/')
# async def upload_image(file: UploadFile = File(...)):
    # Bepaal de locatie waar het bestand wordt opgeslagen
    # file_location = os.path.join(os.path.dirname(__file__), '../frontend/img/met_db', file.filename)
   
    # Controleer of de map bestaat, zo niet, maak deze aan
    # os.makedirs(os.path.dirname(file_location), exist_ok=True)
   
    # Sla het bestand op
    # with open(file_location, "wb") as f:
    #     f.write(await file.read())
    # upload_result = cloudinary.uploader.upload(file.read())
    # img_url = upload_result[""]
    # return {"info": f"file '{file.filename}' saved at '{file_location}'", 'name': file.filename}

@app.post(ENDPOINT + 'fotoToFolder/')
async def upload_image(file: UploadFile = File(...)):
    try:
        # Upload naar Cloudinary
        upload_result = cloudinary.uploader.upload(file.file)
        img_url = upload_result.get("secure_url")
 
        return {
            "message": f"Afbeelding '{file.filename}' succesvol geüpload.",
            "url": img_url,
            "name": file.filename
        }
    except Exception as e:
        return {"error": str(e)}

@app.post(ENDPOINT + 'fotoToDB/', response_model=dict, status_code=status.HTTP_201_CREATED, summary="Foto toevoegen aan database")
async def nieuw_fotot(Foto: DTOFotoToDB):
    response_id = DataRepository.create_foto_pad(Foto.paden)
    if response_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Foto niet gevonden")
    
    data = DataRepository.read_foto_pad()
    send_fotos_en_teksten_via_sio()
    return JSONResponse(content=data)

@app.post(ENDPOINT + 'tekstje/', response_model=list[tekst], status_code=status.HTTP_201_CREATED, summary="Tekstje toevoegen")
async def nieuw_tekst(Tekst: DTOTekst):
    response_id = DataRepository.create_tekst(Tekst.tekstje, Tekst.idfoto)
    if response_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tekst niet gevonden")
    
    data = DataRepository.read_tekst()
    send_fotos_en_teksten_via_sio()
    return data


if __name__ == "__main__":
    import uvicorn
    # Start de server met reload en debug
    uvicorn.run("app:sio_app", host="0.0.0.0", port=8000, log_level="info", reload=True,reload_dirs=["backend"])