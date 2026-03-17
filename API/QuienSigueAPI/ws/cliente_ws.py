from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from dominio.cliente_dominio import ClienteDominio
from dto.cliente_dto import ClienteCreate
import shutil
import os

router = APIRouter()

# --- REGISTRAR ---
@router.post("/registrar")
async def registrar_cliente(
    nombre: str = Form(...),
    apellido_paterno: str = Form(...),
    apellido_materno: str = Form(None),
    fecha_nacimiento: str = Form(...),
    telefono: str = Form(...),
    numero_cliente: str = Form(...),
    archivo_qr: UploadFile = File(...)
):
    folder = "qrcodes"
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    nombre_archivo = f"{numero_cliente}.png"
    ruta_archivo = os.path.join(folder, nombre_archivo)
    
    with open(ruta_archivo, "wb") as buffer:
        shutil.copyfileobj(archivo_qr.file, buffer)

    nuevo_cliente = ClienteCreate(
        nombre=nombre,
        apellido_paterno=apellido_paterno,
        apellido_materno=apellido_materno,
        fecha_nacimiento=fecha_nacimiento,
        telefono=telefono,
        numero_cliente=numero_cliente
    )

    # El dominio ahora debe manejar la inserción con el campo visitas_disponibles
    if ClienteDominio.registrar(nuevo_cliente, ruta_archivo):
        return {
            "status": "ok", 
            "msg": "Cliente registrado correctamente",
            "qr_url": f"http://127.0.0.1:8000/qrcodes/{nombre_archivo}"
        }
    
    raise HTTPException(status_code=400, detail="Error al registrar en la base de datos")

# --- VER TODOS (Ahora incluye visitas_disponibles) ---
@router.get("/")
def ver_clientes():
    """
    Retorna la lista de clientes. 
    Asegúrate de que ClienteDominio.obtener_todos() haga:
    SELECT *, visitas_disponibles FROM clientes
    """
    clientes = ClienteDominio.obtener_todos()
    return clientes

# --- ELIMINAR CLIENTE ---
@router.delete("/eliminar/{id_cliente}")
def eliminar_cliente(id_cliente: int):
    if ClienteDominio.eliminar(id_cliente):
        return {"msg": f"Cliente con ID {id_cliente} eliminado"}
    raise HTTPException(status_code=404, detail="No se pudo eliminar el cliente")

# --- ACTUALIZAR CLIENTE ---
@router.put("/actualizar/{id_cliente}")
def actualizar_cliente(id_cliente: int, datos: ClienteCreate):
    if ClienteDominio.actualizar(id_cliente, datos):
        return {"status": "ok", "msg": "Datos actualizados correctamente"}
    raise HTTPException(status_code=400, detail="No se pudo actualizar el cliente")

@router.get("/proximo-id")
def obtener_id_sugerido():
    nuevo_id = ClienteDominio.generar_siguiente_qs_id()
    return {"siguiente_id": nuevo_id}

@router.put("/{id_cliente}/restar-visita")
def restar_visita(id_cliente: int):
    exito = ClienteDominio.registrar_asistencia(id_cliente)
    if exito:
        return {"status": "success", "message": "Visita descontada correctamente"}
    else:
        # Si no hubo éxito, es porque ya tenía 0 visitas
        raise HTTPException(status_code=400, detail="El cliente no tiene visitas disponibles")
    
@router.put("/{id_cliente}/renovar")
def renovar_cliente(id_cliente: int):
    exito = ClienteDominio.renovar_suscripcion(id_cliente)
    if exito:
        return {"status": "success", "message": "Suscripción renovada"}
    else:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")