import customtkinter as ctk

class LoginView(ctk.CTkFrame):
    def __init__(self, master, controlador):
        super().__init__(master, fg_color="transparent")
        self.controlador = controlador

        self.card = ctk.CTkFrame(self, width=380, height=480, corner_radius=20)
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)

        ctk.CTkLabel(self.card, text="QUIÉN SIGUE", font=("Inter", 30, "bold"), text_color="#3498db").pack(pady=(40, 20))

        self.user_entry = ctk.CTkEntry(self.card, placeholder_text="Usuario", width=280, height=45)
        self.user_entry.pack(pady=10)

        self.pass_entry = ctk.CTkEntry(self.card, placeholder_text="Contraseña", show="*", width=280, height=45)
        self.pass_entry.pack(pady=10)

        self.btn_login = ctk.CTkButton(self.card, text="Iniciar Sesión", width=280, height=45, 
                                       command=self.on_login_click, font=("Inter", 14, "bold"))
        self.btn_login.pack(pady=30)

    def on_login_click(self):
        u, p = self.user_entry.get(), self.pass_entry.get()
        self.btn_login.configure(state="disabled", text="Verificando...")
        
        # El controlador decidirá si destruye esta vista
        self.controlador.validar_login(u, p)
        
        # FIX: Solo reconfigurar si la vista sigue viva tras la petición
        if self.winfo_exists():
            self.btn_login.configure(state="normal", text="Iniciar Sesión")