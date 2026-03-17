import customtkinter as ctk
from tkinter import messagebox

class VisitasView(ctk.CTkFrame):
    def __init__(self, master, controlador):
        super().__init__(master, fg_color="transparent")
        self.controlador = controlador
        
        self.setup_ui()
        # Enfocar el campo de entrada automáticamente para el lector QR
        self.after(100, lambda: self.qr_entry.focus_set())

    def setup_ui(self):
        # Contenedor central
        self.main_container = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=15)
        self.main_container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.6)

        # Icono visual
        self.icon_label = ctk.CTkLabel(self.main_container, text="📸", font=("Inter", 80))
        self.icon_label.pack(pady=(40, 10))

        # Títulos
        ctk.CTkLabel(self.main_container, text="REGISTRO DE ACCESO", 
                     font=("Inter", 24, "bold"), text_color="#3498db").pack()
        
        ctk.CTkLabel(self.main_container, text="Coloque el código QR frente al lector", 
                     font=("Inter", 14), text_color="gray").pack(pady=5)

        # Campo de entrada para el lector QR (simula entrada de teclado)
        self.qr_entry = ctk.CTkEntry(self.main_container, width=300, placeholder_text="Esperando lectura...")
        self.qr_entry.pack(pady=30)
        
        # Vincular la tecla 'Enter' (que los lectores envían al final del código)
        self.qr_entry.bind("<Return>", self.procesar_lectura)

        # Botón de ayuda manual
        self.btn_manual = ctk.CTkButton(self.main_container, text="Procesar Manualmente", 
                                        command=lambda: self.procesar_lectura(None),
                                        fg_color="#2c3e50", hover_color="#34495e")
        self.btn_manual.pack(pady=10)

    def procesar_lectura(self, event):
        codigo = self.qr_entry.get().strip()
        if codigo:
            # Enviar al controlador principal
            self.controlador.on_qr_scanned(codigo)
            # Limpiar para la siguiente lectura
            self.qr_entry.delete(0, 'end')
            self.qr_entry.focus_set()
        else:
            messagebox.showwarning("Atención", "El código QR está vacío.")