from pydantic import BaseModel
from typing import Optional

class VisitaGestion(BaseModel):
    numero_cliente: str
    accion: str  # "descontar" o "cancelar"