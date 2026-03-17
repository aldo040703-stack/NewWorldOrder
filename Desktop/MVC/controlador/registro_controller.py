import qrcode
import os
from tkinter import messagebox

class RegistroController:
    def __init__(self, app):
        self.app = app
        # Reutilizamos el ApiService que ya tienes
        from servicios.api_service import ApiService
        self.api = ApiService()

    def procesar_alta(self, datos, vista_formulario):
        """
        Lógica funcional: Genera QR local y sube a la API.
        """
        # 1. Validación de campos (doble check)
        if not all(datos.values()):
            messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
            return

        try:
            # 2. Generar código QR temporal
            # El QR contiene el ID del cliente para el escaneo futuro
            nombre_qr = f"temp_qr_{datos['numero_cliente']}.png"
            qr = qrcode.make(datos['numero_cliente'])
            qr.save(nombre_qr)

            # 3. Llamar al API Service (Método registrar_cliente que ya definimos)
            exito, mensaje = self.api.registrar_cliente(datos, nombre_qr)

            if exito:
                messagebox.showinfo("Éxito", "Cliente guardado y QR generado correctamente.")
                
                # Borrar archivo temporal local
                if os.path.exists(nombre_qr):
                    os.remove(nombre_qr)
                
                # 4. Limpiar formulario y volver a la vista principal de clientes
                vista_formulario.limpiar_campos()
                self.app.controlador.cambiar_vista("clientes")
            else:
                messagebox.showerror("Error de API", mensaje)
                if os.path.exists(nombre_qr): os.remove(nombre_qr)

        except Exception as e:
            messagebox.showerror("Error de Sistema", f"Ocurrió un error inesperado: {e}")