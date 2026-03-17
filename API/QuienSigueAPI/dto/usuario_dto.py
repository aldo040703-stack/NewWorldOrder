from pydantic import BaseModel
from typing import Optional

class UsuarioBase(BaseModel):
    username: str

class UsuarioCreate(UsuarioBase):
    password: str # Contraseña en texto plano que el backend recibirá

class UsuarioUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None

class UsuarioResponse(UsuarioBase):
    id_usuario: int

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str