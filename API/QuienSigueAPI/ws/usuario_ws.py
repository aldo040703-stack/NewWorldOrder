from fastapi import APIRouter, HTTPException, Body, Depends
from dominio.usuario_dominio import UsuarioDominio
from dto.usuario_dto import UsuarioCreate, UsuarioUpdate, LoginRequest, UsuarioResponse
from typing import List

router = APIRouter()

# --- LOGIN ---
@router.post("/login")
def login(credenciales: LoginRequest):
    """
    Endpoint para autenticar a los usuarios de la app de escritorio.
    """
    usuario = UsuarioDominio.validar_acceso(credenciales.username, credenciales.password)
    if usuario:
        return {
            "status": "success", 
            "mensaje": f"Bienvenido {usuario['username']}",
            "usuario": usuario['username']
        }
    raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

# --- VER TODOS LOS USUARIOS ---
@router.get("/", response_model=List[UsuarioResponse])
def ver_usuarios():
    return UsuarioDominio.obtener_todos()

# --- AGREGAR USUARIO ---
@router.post("/agregar")
def agregar_usuario(usuario: UsuarioCreate):
    if UsuarioDominio.crear(usuario):
        return {"status": "ok", "msg": "Usuario creado exitosamente"}
    raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")

# --- MODIFICAR USUARIO ---
@router.put("/modificar/{id_usuario}")
def modificar_usuario(id_usuario: int, datos: UsuarioUpdate):
    # Convertimos el DTO a diccionario eliminando valores Nulos
    datos_dict = datos.dict(exclude_unset=True)
    if UsuarioDominio.actualizar(id_usuario, datos_dict):
        return {"msg": "Datos de usuario actualizados"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# --- ELIMINAR USUARIO ---
@router.delete("/eliminar/{id_usuario}")
def eliminar_usuario(id_usuario: int):
    if UsuarioDominio.borrar(id_usuario):
        return {"msg": "Usuario eliminado correctamente"}
    raise HTTPException(status_code=404, detail="No se pudo eliminar el usuario")