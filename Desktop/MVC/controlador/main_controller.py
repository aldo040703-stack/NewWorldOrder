from tkinter import messagebox
import os
import qrcode

# Importación de Servicios y Controladores especializados
from servicios.api_service import ApiService
from controlador.usuario_controller import UsuarioController 
from controlador.notificacion_controller import NotificacionController
from controlador.visita_controller import VisitaController

class MainController:
    def __init__(self, app):
        self.app = app
        self.api = ApiService()
        
        # Carpeta persistente para los QR
        self.ruta_qrs = "qrcodes_clientes"
        if not os.path.exists(self.ruta_qrs):
            os.makedirs(self.ruta_qrs)
        
        # Instancia de todos los controladores hijos
        self.usuario_controlador = UsuarioController(self)
        self.notificador = NotificacionController(self.api)
        self.visita_controlador = VisitaController(self)

    # --- SISTEMA DE LOGIN Y NOTIFICACIONES ---
    def validar_login(self, usuario, password):
        """Procesa el acceso y dispara alertas iniciales"""
        if not usuario or not password:
            messagebox.showwarning("Atención", "Llene todos los campos")
            return
        
        exito, resultado = self.api.login(usuario, password)
        
        if exito:
            self.app.mostrar_dashboard()
            self.notificador.verificar_eventos_del_dia()
        else:
            msj = resultado.get("detail") if isinstance(resultado, dict) else resultado
            messagebox.showerror("Error", msj)

    # --- NAVEGACIÓN ENTRE MÓDULOS ---
    def cambiar_vista(self, seccion):
        """Maneja el intercambio de módulos en el panel central"""
        dashboard = self.app.vista_actual
        
        for widget in dashboard.content.winfo_children():
            widget.destroy()

        if seccion == "clientes":
            from vista.clientes_view import ClientesView
            nueva_vista = ClientesView(dashboard.content, self)
            nueva_vista.pack(expand=True, fill="both")
        
        elif seccion == "usuarios":
            from vista.usuarios_view import UsuariosView
            nueva_vista = UsuariosView(dashboard.content, self.usuario_controlador)
            nueva_vista.pack(expand=True, fill="both")

        elif seccion == "notificaciones":
            from vista.notificaciones_view import NotificacionesView
            nueva_vista = NotificacionesView(dashboard.content, self)
            nueva_vista.pack(expand=True, fill="both")
            
        elif seccion == "registrar_visitas":
            from vista.visitas_view import VisitasView
            nueva_vista = VisitasView(dashboard.content, self)
            nueva_vista.pack(expand=True, fill="both")

    def logout(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Seguro que desea salir?"):
            self.app.mostrar_login()

    # --- MÉTODOS DE LÓGICA DE CLIENTES (CON PERSISTENCIA) ---
    def cargar_lista_clientes(self):
        return self.api.obtener_clientes()

    def procesar_registro_cliente(self, datos):
        """Genera QR de forma persistente y registra al cliente"""
        # 1. Definir ruta permanente: qrcodes_clientes/QR_123.png
        nombre_archivo = f"QR_{datos['numero_cliente']}.png"
        ruta_final = os.path.join(self.ruta_qrs, nombre_archivo)
        
        # 2. Generar el QR físicamente
        qr = qrcode.make(datos['numero_cliente'])
        qr.save(ruta_final)
        
        # 3. Registrar en la API
        exito, msj = self.api.registrar_cliente(datos, ruta_final)
        
        if exito:
            # NO BORRAMOS EL ARCHIVO (os.remove eliminado para persistencia)
            messagebox.showinfo("Éxito", f"Cliente registrado.\nQR guardado en: {ruta_final}")
            self.cambiar_vista("clientes") 
        else:
            messagebox.showerror("Error", msj)

    def actualizar_cliente(self, id_cliente, nuevos_datos):
        resultado = self.api.actualizar_cliente(id_cliente, nuevos_datos)
        if resultado.get("status") == "ok":
            messagebox.showinfo("Éxito", "Cliente actualizado")
            self.cambiar_vista("clientes")
            return True
        return False

    def borrar_cliente(self, id_cliente):
        if messagebox.askyesno("Confirmar", "¿Eliminar cliente definitivamente?"):
            if self.api.eliminar_cliente(id_cliente):
                messagebox.showinfo("Éxito", "Cliente eliminado")
                self.cambiar_vista("clientes")

    # --- EVENTO DEL LECTOR QR ---
    def on_qr_scanned(self, codigo):
        # Limpiamos el código por si trae espacios o saltos de línea del lector
        codigo_limpio = str(codigo).strip()
        self.visita_controlador.procesar_lectura_qr(codigo_limpio)

    # --- UTILIDAD DE MANTENIMIENTO ---
    def regenerar_qrs_faltantes(self):
        """Recupera los archivos QR de los clientes que ya están en la BD pero no tienen archivo local"""
        clientes = self.api.obtener_clientes()
        contador = 0
        
        for c in clientes:
            num = c['numero_cliente']
            ruta = os.path.join(self.ruta_qrs, f"QR_{num}.png")
            
            if not os.path.exists(ruta):
                qr = qrcode.make(num)
                qr.save(ruta)
                contador += 1
        
        if contador > 0:
            messagebox.showinfo("Mantenimiento", f"Se han regenerado {contador} códigos QR faltantes.")
        else:
            messagebox.showinfo("Mantenimiento", "Todos los códigos QR están al día.")