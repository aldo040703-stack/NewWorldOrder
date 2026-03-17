from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

# 1. Importar los routers (Añadimos visita_ws)
from ws import cliente_ws, usuario_ws, notificacion_ws, visita_ws # <-- AGREGADO

app = FastAPI(title="Quien Sigue API")

# --- CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS ---
# Esto permite que la app de escritorio descargue el QR si es necesario
if not os.path.exists("qrcodes"):
    os.makedirs("qrcodes")

app.mount("/qrcodes", StaticFiles(directory="qrcodes"), name="qrcodes")

# --- RUTAS ---
@app.get("/")
def root():
    return {"mensaje": "API Funcionando Correctamente"}

# 2. Registrar rutas
app.include_router(cliente_ws.router, prefix="/clientes", tags=["Clientes"])
app.include_router(usuario_ws.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(notificacion_ws.router, prefix="/notificaciones", tags=["Notificaciones"])
app.include_router(visita_ws.router, prefix="/visitas", tags=["Visitas"]) # <-- AGREGADO

# --- INICIO DEL SERVIDOR ---
if __name__ == "__main__":
    print("--- Servidor Iniciado en http://127.0.0.1:8000 ---")
    # Cambia a host="0.0.0.0" si quieres que sea visible en tu red local (WiFi)
    uvicorn.run(app, host="127.0.0.1", port=8000)