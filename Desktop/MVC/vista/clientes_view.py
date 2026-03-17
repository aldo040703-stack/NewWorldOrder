import customtkinter as ctk
from PIL import Image
import requests
from io import BytesIO
import os
from tkinter import messagebox  # Importante para los cuadros de diálogo

# Importación adaptativa del controlador
try:
    from controlador.registro_controller import RegistroController
except ImportError:
    from MVC.controlador.registro_controller import RegistroController

class ClientesView(ctk.CTkFrame):
    def __init__(self, master, controlador_principal):
        super().__init__(master, fg_color="transparent")
        self.controlador_principal = controlador_principal
        self.reg_controlador = RegistroController(controlador_principal.app)

        # Contenedor de pestañas
        self.tabview = ctk.CTkTabview(self, width=950)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

        self.tab_registrar = self.tabview.add("Registrar Nuevo")
        self.tab_gestion = self.tabview.add("Gestionar Clientes")

        self.setup_registrar()
        self.setup_gestion()

    # --- SECCIÓN: REGISTRO ---
    def setup_registrar(self):
        container = ctk.CTkFrame(self.tab_registrar, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(container, text="DATOS DEL CLIENTE", font=("Inter", 20, "bold")).pack(pady=15)

        self.entry_nombre = self._crear_campo(container, "Nombre(s)")
        self.entry_apellido = self._crear_campo(container, "Apellido Paterno")
        self.entry_fecha = self._crear_campo(container, "Fecha Nacimiento (AAAA-MM-DD)")
        self.entry_tel = self._crear_campo(container, "Teléfono")
        
        self.entry_id = self._crear_campo(container, "Número de Cliente (ID)")
        self.cargar_id_automatico()

        self.btn_guardar = ctk.CTkButton(
            container, text="REGISTRAR Y GENERAR QR", height=45, 
            fg_color="#2ecc71", hover_color="#27ae60", font=("Inter", 14, "bold"),
            command=self.enviar_datos_registro
        )
        self.btn_guardar.pack(pady=25, fill="x")

    def _crear_campo(self, master, placeholder):
        e = ctk.CTkEntry(master, placeholder_text=placeholder, width=350, height=35)
        e.pack(pady=5)
        return e

    def cargar_id_automatico(self):
        try:
            response = requests.get("http://127.0.0.1:8000/clientes/proximo-id", timeout=3)
            if response.status_code == 200:
                nuevo_id = response.json().get("siguiente_id", "QS-001")
                self.entry_id.delete(0, 'end')
                self.entry_id.insert(0, nuevo_id)
        except Exception:
            self.entry_id.delete(0, 'end')
            self.entry_id.insert(0, "QS-ERR")

    def enviar_datos_registro(self):
        datos = {
            "nombre": self.entry_nombre.get(),
            "apellido_paterno": self.entry_apellido.get(),
            "fecha_nacimiento": self.entry_fecha.get(),
            "telefono": self.entry_tel.get(),
            "numero_cliente": self.entry_id.get()
        }
        self.reg_controlador.procesar_alta(datos, self)

    def limpiar_campos(self):
        for entry in [self.entry_nombre, self.entry_apellido, self.entry_fecha, self.entry_tel]:
            entry.delete(0, 'end')
        self.cargar_id_automatico()
        self.refrescar_tabla()

    # --- SECCIÓN: GESTIÓN ---
    def setup_gestion(self):
        header = ctk.CTkFrame(self.tab_gestion, fg_color="transparent")
        header.pack(fill="x", pady=10)

        self.search_entry = ctk.CTkEntry(header, placeholder_text="Buscar cliente por nombre o ID...", width=400)
        self.search_entry.pack(side="left", padx=20)
        self.search_entry.bind("<KeyRelease>", lambda e: self.refrescar_tabla())

        ctk.CTkButton(header, text="↻", width=40, command=self.refrescar_tabla).pack(side="right", padx=20)

        self.scroll_lista = ctk.CTkScrollableFrame(self.tab_gestion, height=450)
        self.scroll_lista.pack(fill="both", expand=True, padx=20, pady=10)
        self.refrescar_tabla()

    def refrescar_tabla(self):
        for widget in self.scroll_lista.winfo_children():
            widget.destroy()

        clientes = self.controlador_principal.cargar_lista_clientes()
        busqueda = self.search_entry.get().lower()
        
        for c in clientes:
            nombre_completo = f"{c.get('nombre','')} {c.get('apellido_paterno','')}".lower()
            num_cli = str(c.get('numero_cliente','')).lower()

            if busqueda and (busqueda not in nombre_completo and busqueda not in num_cli):
                continue

            f = ctk.CTkFrame(self.scroll_lista)
            f.pack(fill="x", pady=3, padx=5)
            
            visitas = c.get('visitas_disponibles', 0)
            info = f"{c.get('numero_cliente','S/N')} | {c.get('nombre','')} {c.get('apellido_paterno','')} | Visitas: {visitas}"
            ctk.CTkLabel(f, text=info, font=("Inter", 13)).pack(side="left", padx=15)

            ctk.CTkButton(f, text="Eliminar", fg_color="#e74c3c", hover_color="#c0392b", width=70,
                          command=lambda cid=c['id_cliente']: self.confirmar_eliminacion(cid)).pack(side="right", padx=5)
            
            ctk.CTkButton(f, text="Editar", fg_color="#3498db", hover_color="#2980b9", width=70,
                          command=lambda d=c: VentanaEditar(self, d)).pack(side="right", padx=5)
            
            ctk.CTkButton(f, text="Ver Datos", fg_color="#2ecc71", hover_color="#27ae60", width=80,
                          command=lambda d=c: VentanaDetalles(self, d)).pack(side="right", padx=5)

    def confirmar_eliminacion(self, id_cliente):
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar este cliente?"):
            self.controlador_principal.borrar_cliente(id_cliente)
            self.refrescar_tabla()

# --- VENTANA: MODIFICAR DATOS ---
class VentanaEditar(ctk.CTkToplevel):
    def __init__(self, master, datos):
        super().__init__(master)
        self.master_view = master
        self.id_cliente = datos.get('id_cliente')
        self.title(f"Editar Cliente: {datos.get('nombre')}")
        self.geometry("400x580")
        self.attributes("-topmost", True)
        self.focus()

        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(self.main_frame, text="MODIFICAR DATOS", font=("Inter", 16, "bold")).pack(pady=15)

        self.ent_nombre = self._campo("Nombre", datos.get('nombre'))
        self.ent_apellido = self._campo("Apellido Paterno", datos.get('apellido_paterno'))
        self.ent_tel = self._campo("Teléfono", datos.get('telefono'))
        self.ent_fecha = self._campo("Fecha Nac. (AAAA-MM-DD)", datos.get('fecha_nacimiento'))
        
        self.numero_cliente = datos.get('numero_cliente')

        ctk.CTkButton(self.main_frame, text="GUARDAR CAMBIOS", fg_color="#3498db", 
                      hover_color="#2980b9", font=("Inter", 13, "bold"), height=40,
                      command=self.guardar).pack(pady=30, fill="x", padx=20)

    def _campo(self, label, valor):
        ctk.CTkLabel(self.main_frame, text=label, font=("Inter", 11)).pack(anchor="w", padx=25)
        e = ctk.CTkEntry(self.main_frame, width=300)
        e.insert(0, str(valor) if valor else "")
        e.pack(fill="x", padx=25, pady=(0, 10))
        return e

    def guardar(self):
        nuevos_datos = {
            "nombre": self.ent_nombre.get(),
            "apellido_paterno": self.ent_apellido.get(),
            "telefono": self.ent_tel.get(),
            "fecha_nacimiento": self.ent_fecha.get(),
            "numero_cliente": self.numero_cliente
        }
        
        if self.master_view.controlador_principal.actualizar_cliente(self.id_cliente, nuevos_datos):
            messagebox.showinfo("Éxito", "Datos actualizados correctamente")
            self.master_view.refrescar_tabla()
            self.destroy()

# --- VENTANA: VER DATOS (CON QR, RESTRICCIÓN Y RENOVACIÓN) ---
class VentanaDetalles(ctk.CTkToplevel):
    def __init__(self, master, datos):
        super().__init__(master)
        self.master_view = master
        self.id_db = datos.get('id_cliente')
        self.id_control = str(datos.get('numero_cliente', ''))
        self.nombre_completo = f"{datos.get('nombre', '')} {datos.get('apellido_paterno', '')}"
        self.visitas = datos.get('visitas_disponibles', 0)
        # Extraemos la fecha de vencimiento que viene de la base de datos
        self.fecha_vence = datos.get('fecha_vencimiento', 'No definida')
        
        self.title(f"Expediente: {self.id_control}")
        self.geometry("450x800")  # Aumenté un poco el alto para la nueva info
        self.attributes("-topmost", True)
        self.focus()
        
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(self.main_frame, text="EXPEDIENTE DIGITAL", font=("Inter", 18, "bold")).pack(pady=15)

        # Formatear datos básicos
        fecha_n_raw = datos.get('fecha_nacimiento')
        fecha_nac = str(fecha_n_raw) if fecha_n_raw else "No registrada"

        # Label de información detallada
        self.lbl_info = ctk.CTkLabel(self.main_frame, text="", justify="left", font=("Inter", 13))
        self.lbl_info.pack(pady=10)
        self.actualizar_texto_info(
            datos.get('nombre', ''), 
            datos.get('apellido_paterno', ''), 
            datos.get('telefono', 'N/A'), 
            fecha_nac
        )

        # Indicador de Visitas
        self.lbl_visitas = ctk.CTkLabel(self.main_frame, text="", font=("Inter", 16, "bold"))
        self.lbl_visitas.pack(pady=5)

        # --- SECCIÓN DE FECHA DE VENCIMIENTO ---
        self.lbl_vencimiento = ctk.CTkLabel(
            self.main_frame, 
            text=f"VENCE EL: {self.fecha_vence}", 
            font=("Inter", 12, "italic")
        )
        self.lbl_vencimiento.pack(pady=(0, 15))
        
        # Botón para registrar asistencia
        self.btn_asistencia = ctk.CTkButton(
            self.main_frame, text="REGISTRAR ASISTENCIA", 
            fg_color="#3498db", hover_color="#2980b9", height=45,
            command=self.confirmar_asistencia
        )
        self.btn_asistencia.pack(pady=5, fill="x", padx=40)

        # Botón para renovar
        self.btn_renovar = ctk.CTkButton(
            self.main_frame, text="RENOVAR SUSCRIPCIÓN (+4)", 
            fg_color="#2ecc71", hover_color="#27ae60", height=45,
            command=self.confirmar_renovacion
        )

        self.lbl_qr = ctk.CTkLabel(self.main_frame, text="Cargando QR...")
        self.lbl_qr.pack(pady=15)

        self.actualizar_interfaz_visitas()
        self.cargar_qr_seguro()

    def actualizar_texto_info(self, nombre, apellido, tel, fecha_n):
        info = (f"ID Control: {self.id_control}\n\n"
                f"Nombre: {nombre} {apellido}\n\n"
                f"Teléfono: {tel}\n\n"
                f"F. Nacimiento: {fecha_n}")
        self.lbl_info.configure(text=info)

    def actualizar_interfaz_visitas(self):
        # Si no hay visitas o la fecha ya pasó (esto lo valida la API pero refrescamos UI)
        if self.visitas <= 0:
            color = "#e74c3c"
            texto = "SUSCRIPCIÓN AGOTADA / VENCIDA"
            self.btn_asistencia.configure(state="disabled", fg_color="#95a5a6")
            # Mostramos el botón de renovación si no hay visitas
            self.btn_renovar.pack(pady=5, fill="x", padx=40, before=self.lbl_qr)
        else:
            color = "#2ecc71" if self.visitas > 1 else "#f39c12"
            texto = f"VISITAS DISPONIBLES: {self.visitas}"
            self.btn_asistencia.configure(state="normal", fg_color="#3498db")
            self.btn_renovar.pack_forget() # Ocultamos renovar si aún tiene saldo
        
        self.lbl_visitas.configure(text=texto, text_color=color)

    def confirmar_asistencia(self):
        pregunta = f"¿Registrar entrada para {self.nombre_completo}?\nSe descontará 1 visita."
        if messagebox.askyesno("Confirmar Asistencia", pregunta):
            self.ejecutar_asistencia()

    def confirmar_renovacion(self):
        pregunta = f"¿Deseas renovar la suscripción de {self.nombre_completo}?\nSe añadirán 4 visitas y 30 días de vigencia."
        if messagebox.askyesno("Confirmar Renovación", pregunta):
            self.ejecutar_renovacion()

    def ejecutar_asistencia(self):
        try:
            url = f"http://127.0.0.1:8000/clientes/{self.id_db}/restar-visita"
            response = requests.put(url, timeout=5)
            if response.status_code == 200:
                self.visitas = max(0, self.visitas - 1)
                self.actualizar_interfaz_visitas()
                self.master_view.refrescar_tabla()
            else:
                # Si la API responde error (ej. porque ya venció la fecha)
                error_msg = response.json().get("detail", "No se pudo registrar la visita.")
                messagebox.showwarning("Atención", error_msg)
        except Exception as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar con el servidor: {e}")

    def ejecutar_renovacion(self):
        try:
            url = f"http://127.0.0.1:8000/clientes/{self.id_db}/renovar"
            response = requests.put(url, timeout=5)
            if response.status_code == 200:
                # Actualizamos localmente con los datos que asume la renovación
                self.visitas = 4
                # Nota: Idealmente la API debería devolver la nueva fecha_vencimiento
                # Para simplificar, refrescamos la tabla principal para obtener datos frescos al cerrar
                messagebox.showinfo("Éxito", "Suscripción renovada por 30 días (4 visitas).")
                self.master_view.refrescar_tabla()
                self.destroy() # Cerramos para obligar a reabrir con datos nuevos
            else:
                messagebox.showerror("Error", "No se pudo renovar la suscripción.")
        except Exception as e:
            print(f"Error renovar: {e}")

    def cargar_qr_seguro(self):
        try:
            url = f"http://127.0.0.1:8000/qrcodes/{self.id_control}.png"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                img_data = BytesIO(response.content)
                img_pil = Image.open(img_data)
                self.qr_image = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(250, 250))
                self.lbl_qr.configure(image=self.qr_image, text="")
            else:
                self.lbl_qr.configure(text="QR no generado todavía", text_color="#e74c3c")
        except Exception:
            self.lbl_qr.configure(text="Servidor de imágenes offline", text_color="#f39c12")