from tkinter import messagebox

class VisitaController:
    def __init__(self, main_controller):
        self.main = main_controller
        self.api = main_controller.api

    def procesar_lectura_qr(self, codigo_qr):
        """
        Captura el QR y muestra el conteo actualizado desde la BD.
        """
        # 1. Ventana de confirmación inicial
        if messagebox.askyesno("Registro de Visita", f"¿Confirmar entrada para el cliente: {codigo_qr}?"):
            
            # 2. Llamada a la API (esta ya descuenta -1 en la BD)
            exito, res = self.api.gestionar_visita(codigo_qr, "descontar")
            
            if exito:
                # Extraemos el conteo que viene del backend
                visitas_actuales = res.get('restantes', 0)
                
                info_msg = (
                    f"✅ ¡Visita Registrada!\n\n"
                    f"Cliente: {codigo_qr}\n"
                    f"Visitas restantes: {visitas_actuales}" # <--- AQUÍ APARECE EL CONTEO
                )
                
                # 3. Opción de deshacer por si fue un error
                if messagebox.askretrycancel("Éxito", f"{info_msg}\n\n¿Desea CANCELAR y devolver la visita?"):
                    # Si el usuario presiona 'Reintentar', sumamos +1 de nuevo
                    self.api.gestionar_visita(codigo_qr, "cancelar")
                    messagebox.showinfo("Sistema", "Visita revertida. El contador ha vuelto a su estado anterior.")
            else:
                # Si el cliente tiene 0 visitas, la API devuelve un error
                messagebox.showerror("Sin Accesos", f"Error: {res}")