from database import get_db_connection

class VisitaDominio:
    @staticmethod
    def actualizar_contador_visitas(numero_cliente: str, valor: int):
        conexion = get_db_connection()
        if not conexion:
            return False, "Error de conexión a la base de datos"
            
        try:
            cursor = conexion.cursor(dictionary=True)
            
            # 1. Usamos el nombre real: visitas_disponibles
            sql_update = "UPDATE clientes SET visitas_disponibles = visitas_disponibles + %s WHERE numero_cliente = %s"
            cursor.execute(sql_update, (valor, numero_cliente))
            
            # 2. Consultamos el nuevo saldo con el nombre correcto
            sql_select = "SELECT visitas_disponibles FROM clientes WHERE numero_cliente = %s"
            cursor.execute(sql_select, (numero_cliente,))
            fila = cursor.fetchone()
            
            conexion.commit()
            
            if fila:
                # Retornamos el valor de la columna correcta
                return True, fila['visitas_disponibles']
            
            return False, "Cliente no encontrado"
            
        except Exception as e:
            return False, f"Error en BD: {str(e)}"
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()