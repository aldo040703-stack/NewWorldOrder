from database import get_db_connection

class UsuarioDominio:
    @staticmethod
    def validar_acceso(username, password):
        """
        Verifica si las credenciales coinciden con algún usuario en la DB.
        """
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            sql = "SELECT id_usuario, username FROM usuarios WHERE username = %s AND password = %s"
            cursor.execute(sql, (username, password))
            usuario = cursor.fetchone()
            return usuario
        finally:
            conn.close()

    @staticmethod
    def obtener_todos():
        """
        Retorna la lista de todos los usuarios registrados (sin la contraseña).
        """
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id_usuario, username FROM usuarios")
            return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def crear(usuario_dto):
        """
        Registra un nuevo usuario/empleado.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Primero verificamos si el nombre de usuario ya existe
            cursor.execute("SELECT id_usuario FROM usuarios WHERE username = %s", (usuario_dto.username,))
            if cursor.fetchone():
                return False
            
            sql = "INSERT INTO usuarios (username, password) VALUES (%s, %s)"
            cursor.execute(sql, (usuario_dto.username, usuario_dto.password))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def actualizar(id_usuario, datos):
        """
        Actualiza los datos del usuario de forma dinámica.
        """
        if not datos:
            return False
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            campos = [f"{k} = %s" for k in datos.keys()]
            valores = list(datos.values())
            valores.append(id_usuario)
            
            sql = f"UPDATE usuarios SET {', '.join(campos)} WHERE id_usuario = %s"
            cursor.execute(sql, valores)
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @staticmethod
    def borrar(id_usuario):
        """
        Elimina a un usuario del sistema.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()