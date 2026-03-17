import os
import sys
import customtkinter as ctk

# --- PARCHE PARA ERROR TCL/TK (Python 3.13) ---
if sys.platform == "win32":
    base_path = sys.base_prefix
    for lib in ['tcl', 'tk']:
        path = os.path.join(base_path, 'tcl', f'{lib}8.6')
        if os.path.exists(path):
            os.environ[f'{lib.upper()}_LIBRARY'] = path

from vista.login_view import LoginView
from vista.dashboard_view import DashboardView
from controlador.main_controller import MainController

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Quién Sigue - Gym Management")
        self.geometry("1100x650")
        
        # Configuración visual
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Inicializamos Controlador
        self.controlador = MainController(self)
        
        self.vista_actual = None
        self.mostrar_login()

    def mostrar_login(self):
        if self.vista_actual:
            self.vista_actual.destroy()
        self.vista_actual = LoginView(self, self.controlador)
        self.vista_actual.pack(expand=True, fill="both")

    def mostrar_dashboard(self):
        if self.vista_actual:
            self.vista_actual.destroy()
        self.vista_actual = DashboardView(self, self.controlador)
        self.vista_actual.pack(expand=True, fill="both")

if __name__ == "__main__":
    app = App()
    app.mainloop()