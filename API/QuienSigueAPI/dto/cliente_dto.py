from pydantic import BaseModel
from datetime import date
from typing import Optional

class ClienteBase(BaseModel):
    nombre: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    fecha_nacimiento: date
    telefono: str
    numero_cliente: str

class ClienteCreate(ClienteBase):
    pass # Se usa para el registro

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None
    telefono: Optional[str] = None
    visitas_disponibles: Optional[int] = None

class ClienteResponse(ClienteBase):
    id_cliente: int
    visitas_disponibles: int
    qr_path: str

    class Config:
        from_attributes = True