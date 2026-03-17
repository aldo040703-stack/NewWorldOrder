import customtkinter as ctk

class DashboardView(ctk.CTkFrame):
    def __init__(self, master, controlador):
        super().__init__(master, fg_color="transparent")
        self.controlador = controlador

        # --- SIDEBAR (Izquierda) ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.logo_label = ctk.CTkLabel(self.sidebar, text="MENÚ", font=("Inter", 20, "bold"))
        self.logo_label.pack(pady=30)

        # Botones del Menú
        # Nota: Guardamos las referencias por si necesitamos cambiar su color después
        self.btn_clientes = self._crear_boton_menu("Clientes", "clientes")
        # Cambia esta línea:
        self.btn_visitas = self._crear_boton_menu("Registrar Visitas", "registrar_visitas") # <-- Agregamos 'registrar_'        self.btn_usuarios = self._crear_boton_menu("Usuarios", "usuarios")
        self.btn_notif = self._crear_boton_menu("Notificaciones", "notificaciones")

        # Botón Salir (Abajo)
        self.btn_logout = ctk.CTkButton(self.sidebar, text="Cerrar Sesión", fg_color="#e74c3c", 
                                        hover_color="#c0392b", command=self.controlador.logout)
        self.btn_logout.pack(side="bottom", fill="x", padx=20, pady=20)

        # --- CONTENIDO (Derecha) ---
        # Cambiado de self.main_content a self.content para que coincida con el MainController
        self.content = ctk.CTkFrame(self, corner_radius=15, fg_color="#1e1e1e")
        self.content.pack(side="right", expand=True, fill="both", padx=15, pady=15)

        # Label por defecto para que no se vea vacío al inicio
        self.welcome_label = ctk.CTkLabel(self.content, text="Bienvenido al Sistema\nSeleccione una opción del menú", 
                                          font=("Inter", 16), text_color="gray")
        self.welcome_label.place(relx=0.5, rely=0.5, anchor="center")

    def _crear_boton_menu(self, texto, seccion):
        # El truco 's=seccion' dentro del lambda es vital para que cada botón 
        # recuerde a qué sección debe ir.
        btn = ctk.CTkButton(self.sidebar, text=texto, anchor="w", height=40, 
                            fg_color="transparent", hover_color="#2c3e50",
                            command=lambda s=seccion: self.controlador.cambiar_vista(s))
        btn.pack(fill="x", padx=15, pady=5)
        return btn