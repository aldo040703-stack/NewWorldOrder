from database import get_db_connection
from datetime import datetime, timedelta

class ClienteDominio:

    @staticmethod
    def calcular_vencimiento():
        """Calcula la fecha actual más 30 días."""
        return (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')

    @staticmethod
    def obtener_todos():
        conexion = get_db_connection()
        try:
            cursor = conexion.cursor(dictionary=True)
            
            # REGLA DE NEGOCIO: Si la fecha de vencimiento ya pasó, 
            # las visitas se resetean a 0 automáticamente antes de consultar.
            sql_update = "UPDATE clientes SET visitas_disponibles = 0 WHERE fecha_vencimiento < CURDATE()"
            cursor.execute(sql_update)
            conexion.commit()

            sql = """SELECT id_cliente, nombre, apellido_paterno, apellido_materno, 
                     fecha_nacimiento, telefono, numero_cliente, visitas_disponibles, 
                     qr_path, fecha_vencimiento FROM clientes"""
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            conexion.close()

    @staticmethod
    def registrar(cliente, qr_path):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            vencimiento = ClienteDominio.calcular_vencimiento()
            
            # Se registran con 4 visitas y vencimiento a 30 días
            sql = """INSERT INTO clientes (numero_cliente, nombre, apellido_paterno, 
                     apellido_materno, fecha_nacimiento, telefono, qr_path, 
                     visitas_disponibles, fecha_vencimiento) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, 4, %s)"""
            
            cursor.execute(sql, (
                cliente.numero_cliente, cliente.nombre, cliente.apellido_paterno, 
                cliente.apellido_materno, cliente.fecha_nacimiento, cliente.telefono, 
                qr_path, vencimiento
            ))
            conn.commit()
            return True
        finally:
            conn.close()

    @staticmethod
    def actualizar(id_cliente, datos):
        if hasattr(datos, 'model_dump'):
            dict_datos = datos.model_dump(exclude_unset=True)
        elif hasattr(datos, 'dict'):
            dict_datos = datos.dict(exclude_unset=True)
        else:
            dict_datos = datos

        if not dict_datos:
            return False

        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            columnas_permitidas = ['nombre', 'apellido_paterno', 'apellido_materno', 
                                  'fecha_nacimiento', 'telefono', 'numero_cliente']
            dict_datos = {k: v for k, v in dict_datos.items() if k in columnas_permitidas}

            campos = [f"{key} = %s" for key in dict_datos.keys()]
            valores = list(dict_datos.values())
            valores.append(id_cliente)
            
            sql = f"UPDATE clientes SET {', '.join(campos)} WHERE id_cliente = %s"
            cursor.execute(sql, valores)
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error en SQL Update: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_cliente):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id_cliente,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @staticmethod
    def generar_siguiente_qs_id():
        conexion = get_db_connection()
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT MAX(CAST(SUBSTRING(numero_cliente, 4) AS UNSIGNED)) FROM clientes WHERE numero_cliente LIKE 'QS-%'")
            resultado = cursor.fetchone()[0]
            siguiente_num = (resultado + 1) if resultado is not None else 1
            return f"QS-{siguiente_num:03d}"
        finally:
            conexion.close()

    @staticmethod
    def registrar_asistencia(id_cliente):
        conexion = get_db_connection()
        try:
            cursor = conexion.cursor()
            # Solo permite restar si no ha vencido y tiene visitas > 0
            sql = """
                UPDATE clientes 
                SET visitas_disponibles = GREATEST(visitas_disponibles - 1, 0) 
                WHERE id_cliente = %s 
                AND visitas_disponibles > 0 
                AND fecha_vencimiento >= CURDATE()
            """
            cursor.execute(sql, (id_cliente,))
            conexion.commit()
            return cursor.rowcount > 0
        finally:
            conexion.close()

    @staticmethod
    def renovar_suscripcion(id_cliente):
        conexion = get_db_connection()
        try:
            cursor = conexion.cursor()
            nueva_fecha = ClienteDominio.calcular_vencimiento()
            
            # Al renovar, se restauran las 4 visitas y se dan 30 días más desde hoy
            sql = """UPDATE clientes 
                     SET visitas_disponibles = 4, fecha_vencimiento = %s 
                     WHERE id_cliente = %s"""
            cursor.execute(sql, (nueva_fecha, id_cliente))
            conexion.commit()
            return cursor.rowcount > 0
        finally:
            conexion.close()