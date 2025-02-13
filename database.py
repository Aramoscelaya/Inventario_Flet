import threading
#import psycopg2
from config import DB_CONECT, stateArea, stateCategory
import datetime
import json

cursor = DB_CONECT.cursor()


def close_connection():
    if DB_CONECT.is_connected():
        print("✅ Conexión exitosa a MySQL")

    # Cierra la conexión al finalizar
    DB_CONECT.close()
    print("✅ Conexión cerrada a MySQL")

def guardar_codigo(codigo):
    pass#thread = threading.Thread(target=insertar_codigo, args=(codigo))
    #thread.start()

def create_product(data):
    #[{'name': 'id_producto', 'value': 'PF4HD0K'}, {'name': 'modelo', 'value': 'E14'}, {'name': 'marca', 'value': 'Lenovo'}, {'name': 'hostname', 'value': 'WPHI002-LP'}, {'name': 'id_area', 'value': 'Honest'}, {'name': 'id_categoria', 'value': 'Laptop'}, {'name': 'usuario_modificacion', 'value': 'admin'}]
    dataName = []
    dataValue = []

    for items in data:
        
        dataName.append(items['name'])
        if items['name'] == 'id_area':
            value = stateArea[items['value']]
            dataValue.append(value)
        elif items['name'] == 'id_categoria':
            value = stateCategory[items['value']]
            dataValue.append(value)
        else:
            dataValue.append(items['value'])

    sql = 'INSERT INTO productos (nombre_producto, '+', '.join(dataName)+') VALUES ("", %s, %s, %s, %s, %s, %s, %s)'
    valores = (dataValue)

    print(sql)
    print(valores)
    '''
    INSERT INTO productos (id_producto, nombre_producto, modelo, marca, hostname, id_area, id_categoria, usuario_modificacion) VALUES (%s, %s, %s, %s, %s, %s, %s)
    ['PF4HD0K', 'E14', 'Lenovo', 'WPHI002-LP', 5, 3, 'admin']
    '''

    cursor.execute(sql, valores)
    DB_CONECT.commit()  # Guarda los cambios en la base de datos

    print("Registro insertado, ID:", cursor.lastrowid)
    cursor.close()
    close_connection()


    
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