import customtkinter as ctk
from tkinter import messagebox

class UsuariosView(ctk.CTkFrame):
    def __init__(self, master, controlador_usuario):
        super().__init__(master, fg_color="transparent")
        # Aquí 'controlador_usuario' es la instancia de UsuarioController
        self.controlador = controlador_usuario

        # Título del Módulo
        self.label_titulo = ctk.CTkLabel(self, text="GESTIÓN DE USUARIOS", font=("Inter", 24, "bold"))
        self.label_titulo.pack(pady=(20, 0))

        # Pestañas
        self.tabview = ctk.CTkTabview(self, width=800)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

        self.tab_reg = self.tabview.add("Registrar Nuevo")
        self.tab_list = self.tabview.add("Lista de Usuarios")

        self.setup_registro()
        self.setup_lista()

    # --- PESTAÑA 1: REGISTRO ---
    def setup_registro(self):
        container = ctk.CTkFrame(self.tab_reg, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(container, text="DATOS DE ACCESO", font=("Inter", 16, "bold")).pack(pady=10)
        
        self.ent_user = ctk.CTkEntry(container, placeholder_text="Nombre de usuario", width=350, height=40)
        self.ent_user.pack(pady=10)
        
        self.ent_pass = ctk.CTkEntry(container, placeholder_text="Contraseña", show="*", width=350, height=40)
        self.ent_pass.pack(pady=10)

        self.btn_crear = ctk.CTkButton(
            container, text="GUARDAR USUARIO", height=45,
            fg_color="#2ecc71", hover_color="#27ae60", font=("Inter", 14, "bold"),
            command=self.ejecutar_registro
        )
        self.btn_crear.pack(pady=20, fill="x")

    def ejecutar_registro(self):
        user = self.ent_user.get()
        password = self.ent_pass.get()
        self.controlador.registrar_usuario(user, password)
        # Limpiar campos después de intentar
        self.ent_user.delete(0, 'end')
        self.ent_pass.delete(0, 'end')

    # --- PESTAÑA 2: LISTA Y GESTIÓN ---
    def setup_lista(self):
        # Frame de encabezado para búsqueda o refresco
        header = ctk.CTkFrame(self.tab_list, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=10)

        ctk.CTkButton(header, text="Refrescar Lista", width=120, 
                      command=self.refrescar).pack(side="right")

        # Frame scrollable para los usuarios
        self.scroll = ctk.CTkScrollableFrame(self.tab_list)
        self.scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.refrescar()

    def refrescar(self):
        # Limpiar lista actual
        for w in self.scroll.winfo_children():
            w.destroy()

        usuarios = self.controlador.listar_usuarios()
        
        for u in usuarios:
            card = ctk.CTkFrame(self.scroll)
            card.pack(fill="x", pady=5, padx=5)
            
            # Info Usuario
            ctk.CTkLabel(card, text=f"ID: {u['id_usuario']}", font=("Inter", 12, "bold"), width=50).pack(side="left", padx=10)
            ctk.CTkLabel(card, text=f"Usuario: {u['username']}", font=("Inter", 13)).pack(side="left", padx=10)
            
            # Botones
            btn_del = ctk.CTkButton(card, text="Eliminar", fg_color="#e74c3c", hover_color="#c0392b", width=80,
                                    command=lambda id_u=u['id_usuario']: self.controlador.eliminar_cuenta(id_u))
            btn_del.pack(side="right", padx=5, pady=5)
            
            btn_edit = ctk.CTkButton(card, text="Editar", fg_color="#3498db", hover_color="#2980b9", width=80,
                                     command=lambda user=u: VentanaEditarUser(self, user))
            btn_edit.pack(side="right", padx=5, pady=5)

# --- VENTANA EMERGENTE PARA EDITAR CON DOBLE VALIDACIÓN ---
class VentanaEditarUser(ctk.CTkToplevel):
    def __init__(self, master, usuario):
        super().__init__(master)
        self.master_view = master
        self.id_usuario = usuario['id_usuario']
        
        self.title("Modificar Usuario")
        self.geometry("400x500") # Aumentamos un poco la altura
        self.attributes("-topmost", True)
        self.focus()

        ctk.CTkLabel(self, text=f"Editando: {usuario['username']}", font=("Inter", 16, "bold")).pack(pady=20)

        # Campo Nombre
        self.ent_new_name = ctk.CTkEntry(self, placeholder_text="Nuevo nombre", width=300)
        self.ent_new_name.insert(0, usuario['username'])
        self.ent_new_name.pack(pady=10)

        # Campo Contraseña 1
        self.ent_new_pass = ctk.CTkEntry(self, placeholder_text="Nueva contraseña", 
                                         show="*", width=300)
        self.ent_new_pass.pack(pady=10)

        # Campo Contraseña 2 (Confirmación)
        self.ent_confirm_pass = ctk.CTkEntry(self, placeholder_text="Confirmar nueva contraseña", 
                                             show="*", width=300)
        self.ent_confirm_pass.pack(pady=10)

        ctk.CTkLabel(self, text="* Deje las contraseñas en blanco para no cambiarlas", 
                     font=("Inter", 10), text_color="gray").pack()

        btn_save = ctk.CTkButton(self, text="GUARDAR CAMBIOS", fg_color="#3498db",
                                 height=40, font=("Inter", 13, "bold"),
                                 command=self.confirmar_cambios)
        btn_save.pack(pady=30)

    def confirmar_cambios(self):
        nombre = self.ent_new_name.get()
        p1 = self.ent_new_pass.get()
        p2 = self.ent_confirm_pass.get()
        
        # Llamamos al controlador con los nuevos parámetros
        if self.master_view.controlador.actualizar_datos(self.id_usuario, nombre, p1, p2):
            self.destroy()
            self.master_view.refrescar()