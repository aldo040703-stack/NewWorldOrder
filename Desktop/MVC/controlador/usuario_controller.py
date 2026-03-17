from tkinter import messagebox

class UsuarioController:
    def __init__(self, controlador_principal):
        # Referenciamos al principal para usar su api_service y cambiar vistas
        self.main = controlador_principal
        self.api = controlador_principal.api

    def listar_usuarios(self):
        """Módulo: VER"""
        return self.api.obtener_usuarios()

    def registrar_usuario(self, username, password):
        """Módulo: REGISTRAR"""
        if not username or not password:
            messagebox.showwarning("Atención", "Todos los campos son obligatorios")
            return

        datos = {"username": username, "password": password}
        exito, msj = self.api.registrar_usuario(datos)
        
        if exito:
            messagebox.showinfo("Éxito", "Usuario creado correctamente")
            self.main.cambiar_vista("usuarios")
        else:
            messagebox.showerror("Error", msj)

    def actualizar_datos(self, id_usuario, username, pass1, pass2):
   
        
        # 1. Validar que las contraseñas coincidan si se escribió algo
        if pass1 != pass2:
            messagebox.showerror("Error", "Las contraseñas no coinciden. Por favor, verifícalas.")
            return False

        # 2. Preparar datos para el backend
        datos = {"username": username}
        
        # Solo incluimos la contraseña si no está vacía
        if pass1.strip():
            datos["password"] = pass1

        # 3. Llamada a la API
        if self.api.actualizar_usuario(id_usuario, datos):
            messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
            self.main.cambiar_vista("usuarios")
            return True
        else:
            messagebox.showerror("Error", "No se pudo actualizar el usuario")
            return False

    def eliminar_cuenta(self, id_usuario):
        """Módulo: ELIMINAR"""
        if messagebox.askyesno("Confirmar", "¿Deseas eliminar definitivamente este usuario?"):
            if self.api.eliminar_usuario(id_usuario):
                messagebox.showinfo("Éxito", "Usuario eliminado")
                self.main.cambiar_vista("usuarios")
            else:
                messagebox.showerror("Error", "No se pudo completar la acción")