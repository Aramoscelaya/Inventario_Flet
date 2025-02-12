import threading
import psycopg2
from config import DB_CONECT
import datetime


def close_connection():
    if DB_CONECT.is_connected():
        print("✅ Conexión exitosa a MySQL")

    # Cierra la conexión al finalizar
    DB_CONECT.close()
    print("✅ Conexión cerrada a MySQL")

def guardar_codigo(codigo):
    pass#thread = threading.Thread(target=insertar_codigo, args=(codigo))
    #thread.start()

def get_code(code):
    pass

'''
def insertar_codigo(codigo):
    cursor = DB_CONECT.cursor()

    queryIfExist = "SELECT EXISTS (SELECT 1 FROM barcodes WHERE barcode = %s)"
    cursor.execute(queryIfExist, (codigo))
    
    if not cursor:
        query = "INSERT INTO barcodes (barcode, registered_at) VALUES (%s, %s)"
        
        try:
            cursor.execute(query, (codigo, datetime.datetime.now()))
            DB_CONECT.commit()
            print(f"Código {codigo} guardado correctamente.")
        except Exception as e:
            print(f"Error al guardar el código: {e}")
        finally:
            cursor.close()
            DB_CONECT.close()
    else:
        print(f"Código {codigo} existente.")
'''