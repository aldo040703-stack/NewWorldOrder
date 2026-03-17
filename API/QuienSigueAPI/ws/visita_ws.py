from fastapi import APIRouter, HTTPException
from dto.visita_dto import VisitaGestion
from dominio.visita_dominio import VisitaDominio

router = APIRouter()

@router.post("/procesar")
def procesar_visita(datos: VisitaGestion):
    valor = -1 if datos.accion == "descontar" else 1
    exito, resultado = VisitaDominio.actualizar_contador_visitas(datos.numero_cliente, valor)
    
    if exito:
        return {
            "status": "ok", 
            "mensaje": "Operación exitosa", 
            "restantes": resultado # <--- Esto es lo que lee el controlador
        }
    raise HTTPException(status_code=400, detail=resultado)