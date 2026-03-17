import customtkinter as ctk
from controlador.registro_controller import RegistroController

class RegistroClienteView(ctk.CTkFrame):
    def __init__(self, master, app_principal):
        super().__init__(master, fg_color="transparent")
        
        # Guardamos referencia a la App para navegar, 
        # pero creamos nuestro propio controlador de lógica
        self.app_principal = app_principal
        self.reg_controlador = RegistroController(app_principal)

        self.container = ctk.CTkFrame(self, corner_radius=15)
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(self.container, text="ALTA DE CLIENTE", font=("Inter", 22, "bold")).pack(pady=20, padx=40)

        # Entradas de datos
        self.entry_nombre = self._crear_entry("Nombre(s)")
        self.entry_apellido = self._crear_entry("Apellido Paterno")
        self.entry_fecha = self._crear_entry("Fecha Nacimiento (AAAA-MM-DD)")
        self.entry_tel = self._crear_entry("Teléfono")
        self.entry_id = self._crear_entry("ID Cliente (Número de Control)")

        # Botón Guardar
        self.btn_guardar = ctk.CTkButton(
            self.container, text="GUARDAR CLIENTE", height=45, 
            fg_color="#2ecc71", hover_color="#27ae60", font=("Inter", 14, "bold"),
            command=self.enviar_datos
        )
        self.btn_guardar.pack(pady=(30, 10), padx=40, fill="x")

    def _crear_entry(self, placeholder):
        e = ctk.CTkEntry(self.container, placeholder_text=placeholder, width=320, height=40)
        e.pack(pady=8, padx=40)
        return e

    def enviar_datos(self):
        # Recopilamos en un diccionario
        datos = {
            "nombre": self.entry_nombre.get(),
            "apellido_paterno": self.entry_apellido.get(),
            "fecha_nacimiento": self.entry_fecha.get(),
            "telefono": self.entry_tel.get(),
            "numero_cliente": self.entry_id.get()
        }
        # Delegamos la lógica al controlador de registro
        self.reg_controlador.procesar_alta(datos, self)

    def limpiar_campos(self):
        for widget in self.container.winfo_children():
            if isinstance(widget, ctk.CTkEntry):
                widget.delete(0, 'end')