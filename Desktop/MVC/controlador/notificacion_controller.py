from tkinter import messagebox

class NotificacionController:
    def __init__(self, api_service):
        """
        Recibe el servicio API para poder hacer consultas.
        """
        self.api = api_service

    def verificar_eventos_del_dia(self):
        """
        Consulta la API y dispara una alerta si hay clientes de cumpleaños.
        """
        print("DEBUG: Verificando notificaciones de cumpleaños...")
        
        # Llamamos al método que creamos en ApiService
        data = self.api.obtener_alertas_cumpleanos()
        
        # Verificamos si hay cumpleañeros hoy
        if data and data.get("total", 0) > 0:
            cumpleaneros = data.get("cumpleaneros", [])
            
            # Construimos el mensaje con los nombres
            nombres = "\n".join([f"• {c['nombre']}" for c in cumpleaneros])
            
            # Lanzamos la alerta visual
            messagebox.showinfo(
                "Centro de Notificaciones 🎂",
                f"¡Hoy tenemos {data['total']} cliente(s) de cumpleaños!\n\n"
                f"{nombres}\n\n"
                "¿Deseas enviarles una promoción especial?"
            )
        else:
            print("DEBUG: No hay cumpleañeros registrados para hoy.")