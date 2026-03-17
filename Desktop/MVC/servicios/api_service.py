import requests

class ApiService:
    BASE_URL = "http://127.0.0.1:8000"

    # --- SISTEMA DE ACCESO (LOGIN) ---
    def login(self, username, password):
        """Autenticación de usuarios en el sistema"""
        try:
            url = f"{self.BASE_URL}/usuarios/login"
            response = requests.post(url, json={"username": username, "password": password}, timeout=5)
            
            if response.status_code == 200:
                return True, response.json()
            else:
                detail = response.json().get("detail", "Credenciales inválidas")
                return False, detail
        except Exception as e:
            print(f"Error en Login: {e}")
            return False, "Error: No se pudo conectar con la API"

    # --- MÓDULO DE CLIENTES ---
    def obtener_clientes(self):
        """Obtiene la lista de todos los clientes registrados"""
        try:
            url = f"{self.BASE_URL}/clientes/"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Error obtener_clientes: {e}")
            return []

    def registrar_cliente(self, datos, ruta_imagen_qr):
        """Registra un nuevo cliente enviando datos y el archivo QR generado localmente"""
        try:
            url = f"{self.BASE_URL}/clientes/registrar"
            # Se usa 'with' para asegurar que el archivo se cierre tras la lectura
            with open(ruta_imagen_qr, "rb") as f:
                files = {"archivo_qr": (ruta_imagen_qr, f, "image/png")}
                # data=datos envía los campos como form-data para convivir con el archivo
                response = requests.post(url, data=datos, files=files, timeout=10)
            
            if response.status_code == 200:
                return True, "Cliente registrado con éxito"
            else:
                msg = response.json().get("detail", "Error al registrar")
                return False, msg
        except Exception as e:
            print(f"Error registrar_cliente: {e}")
            return False, f"Error de conexión: {str(e)}"

    def actualizar_cliente(self, id_cliente, datos):
        """Envía una petición PUT para modificar los datos de un cliente"""
        try:
            url = f"{self.BASE_URL}/clientes/actualizar/{id_cliente}"
            response = requests.put(url, json=datos, timeout=5)
            
            if response.status_code == 200:
                return {"status": "ok", "msg": "Datos actualizados correctamente"}
            else:
                return {"status": "error", "msg": response.json().get("detail", "Error")}
        except Exception as e:
            print(f"Error actualizar_cliente: {e}")
            return {"status": "error", "msg": str(e)}

    def eliminar_cliente(self, id_cliente):
        """Elimina un cliente de la base de datos por su ID"""
        try:
            url = f"{self.BASE_URL}/clientes/eliminar/{id_cliente}"
            response = requests.delete(url, timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"Error eliminar_cliente: {e}")
            return False

    # --- MÓDULO DE USUARIOS ---
    def obtener_usuarios(self):
        """Obtiene la lista de usuarios del sistema"""
        try:
            response = requests.get(f"{self.BASE_URL}/usuarios/", timeout=5)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Error obtener_usuarios: {e}")
            return []

    def registrar_usuario(self, datos):
        """Registra un nuevo usuario administrativo"""
        try:
            response = requests.post(f"{self.BASE_URL}/usuarios/agregar", json=datos, timeout=5)
            if response.status_code == 200:
                return True, response.json().get("msg", "Éxito")
            
            error_msj = response.json().get("detail", "Error al registrar")
            return False, error_msj
        except Exception as e:
            return False, str(e)

    def actualizar_usuario(self, id_usuario, datos):
        """Actualiza datos de un usuario (incluye validación de contraseña)"""
        try:
            url = f"{self.BASE_URL}/usuarios/modificar/{id_usuario}"
            response = requests.put(url, json=datos, timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"Error actualizar_usuario: {e}")
            return False

    def eliminar_usuario(self, id_usuario):
        """Elimina un usuario por ID"""
        try:
            response = requests.delete(f"{self.BASE_URL}/usuarios/eliminar/{id_usuario}", timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"Error eliminar_usuario: {e}")
            return False

    # --- MÓDULO DE NOTIFICACIONES ---
    def obtener_alertas_cumpleanos(self):
        """Consulta los cumpleañeros del día"""
        try:
            url = f"{self.BASE_URL}/notificaciones/cumpleanos"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error en Notificaciones API: {response.status_code}")
                return {"total": 0, "cumpleaneros": []}
        except Exception as e:
            print(f"Error de conexión en notificaciones: {e}")
            return {"total": 0, "cumpleaneros": []}

    # --- MÓDULO DE VISITAS (NUEVO) ---
    def gestionar_visita(self, numero_cliente, accion="descontar"):
        """
        Envía una petición POST con el DTO de VisitaGestion al servidor FastAPI.
        accion: 'descontar' o 'cancelar'
        """
        try:
            # Asegúrate de que este prefix '/visitas' coincida con tu main.py de la API
            url = f"{self.BASE_URL}/visitas/procesar"
            payload = {
                "numero_cliente": str(numero_cliente),
                "accion": accion
            }
            response = requests.post(url, json=payload, timeout=5)
            
            if response.status_code == 200:
                # El servidor responde con 'status', 'mensaje' y 'restantes'
                return True, response.json()
            else:
                msg = response.json().get("detail", "Error en la operación")
                return False, msg
        except Exception as e:
            print(f"Error ApiService Visitas: {e}")
            return False, "Error de conexión con el servidor"