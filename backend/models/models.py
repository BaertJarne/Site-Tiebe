from pydantic import BaseModel

class foto(BaseModel):
    idfoto_paden: int
    paden: str

class DTOFotoToDB(BaseModel):
    paden: str

class DTOFotoToFolder(BaseModel):
    info: dict

class tekst(BaseModel):
    idtekst: int
    tekstje: str
    idfoto: int

class DTOTekst(BaseModel):
    tekstje: str
    idfoto: int