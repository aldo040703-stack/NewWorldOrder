import customtkinter as ctk

class NotificacionesView(ctk.CTkFrame):
    def __init__(self, master, controlador_principal):
        super().__init__(master, fg_color="transparent")
        self.main = controlador_principal
        self.api = controlador_principal.api
        
        self.setup_ui()
        self.cargar_notificaciones()

    def setup_ui(self):
        # Título del módulo
        ctk.CTkLabel(self, text="Centro de Notificaciones", 
                     font=("Inter", 24, "bold")).pack(pady=20, padx=20, anchor="w")
        
        # Contenedor para las tarjetas de notificación
        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="#1e1e1e", width=600, height=400)
        self.scroll_container.pack(expand=True, fill="both", padx=20, pady=10)

    def cargar_notificaciones(self):
        # Limpiar contenedor
        for widget in self.scroll_container.winfo_children():
            widget.destroy()

        # Obtener datos de la API
        data = self.api.obtener_alertas_cumpleanos()
        
        if data and data.get("total", 0) > 0:
            for c in data.get("cumpleaneros", []):
                self.crear_tarjeta_cumple(c['nombre'])
        else:
            ctk.CTkLabel(self.scroll_container, text="No hay notificaciones pendientes para hoy.",
                         font=("Inter", 14), text_color="gray").pack(pady=50)

    def crear_tarjeta_cumple(self, nombre):
        # Tarjeta visual para cada cumpleañero
        card = ctk.CTkFrame(self.scroll_container, fg_color="#2b2b2b", corner_radius=10)
        card.pack(fill="x", pady=5, padx=5)
        
        emoji = ctk.CTkLabel(card, text="🎂", font=("Inter", 25))
        emoji.pack(side="left", padx=15, pady=10)
        
        texto = ctk.CTkLabel(card, text=f"Hoy es el cumpleaños de {nombre}", 
                             font=("Inter", 14, "bold"), text_color="#3498db")
        texto.pack(side="left", padx=10)
        
        btn_felicitar = ctk.CTkButton(card, text="Felicitar", width=80, height=25,
                                      fg_color="#27ae60", hover_color="#2ecc71")
        btn_felicitar.pack(side="right", padx=15)