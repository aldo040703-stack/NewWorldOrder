from fastapi import APIRouter
from datetime import date
from dominio.cliente_dominio import ClienteDominio

router = APIRouter()

@router.get("/cumpleanos")
def obtener_cumpleanos_hoy():
    try:
        hoy = date.today()
        todos = ClienteDominio.obtener_todos()
        cumpleaneros = []

        for c in todos:
            f_nac = c.get("fecha_nacimiento")
            if not f_nac:
                continue
            
            # Si f_nac ya es un objeto date (por ser tipo DATE en la DB)
            # o si es un string, lo normalizamos:
            try:
                if isinstance(f_nac, str):
                    from datetime import datetime
                    fecha_obj = datetime.strptime(f_nac, "%Y-%m-%d").date()
                else:
                    fecha_obj = f_nac # Ya es un objeto date/datetime
                
                # Comparación de mes y día
                if fecha_obj.month == hoy.month and fecha_obj.day == hoy.day:
                    cumpleaneros.append({
                        "nombre": f"{c['nombre']} {c['apellido_paterno']}"
                    })
            except Exception as ex:
                print(f"Error procesando fecha del cliente {c.get('id_cliente')}: {ex}")
                continue
        
        return {
            "total": len(cumpleaneros),
            "cumpleaneros": cumpleaneros,
            "status": "success"
        }
    except Exception as e:
        print(f"Error crítico en WS Notificaciones: {e}")
        return {"total": 0, "cumpleaneros": [], "status": "error", "msg": str(e)}