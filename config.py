"""DB_CONFIG = {
    "host": "149.50.136.78",
    "port": 5432,
    "database": "barcode_db",
    "user": "root",
    "password": "1234"
}

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "darksus",
    "user": "darksus",
    "password": ""
}


conn = psycopg2.connect(**DB_CONFIG)
print("--------------------------------------------------------------------------")
print(conn)
print("--------------------------------------------------------------------------")
return
"""
import mysql.connector

try:
    DB_CONECT = mysql.connector.connect(
        host="localhost",      # Cambia si usas un servidor remoto
        user="root",     # Usuario de MySQL
        password="0666", # Contraseña de MySQL
        database="Inventario" # Nombre de la base de datos
    )

    print("✅ Conexión exitosa")

    stateArea = {
        'Sistemas': 1,
        'Nexus_Service': 2,
        'Nexus_Sales': 3,
        'Avis': 4,
        'Honest': 5,
        'W2FLY': 6,
    }

    stateCategory = {
        'CPU': 1,
        'UPS': 2,
        'Laptop': 3,
        'Monitor': 4,
    }

except mysql.connector.Error as e:
    print(f"❌ Error conectando a MySQL: {e}")
finally:
    if 'conexion' in locals() and DB_CONECT.is_connected():
        DB_CONECT.close()