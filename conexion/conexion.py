import pymysql

# Credenciales de la base de datos
host = 'bo2hc4epacbxc16ou5of-mysql.services.clever-cloud.com'
user = 'uzzi1lzjkhuq2y92'
password = 'TWwLvF3658qNHnmTU7KX'
database = 'bo2hc4epacbxc16ou5of'
port = 3306

# Conectar a la base de datos
conexion = pymysql.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    port=port,
    cursorclass=pymysql.cursors.DictCursor  # Para obtener los resultados como diccionarios
)

try:
    with conexion.cursor() as cursor:
        # Realizar una consulta de prueba
        cursor.execute("SELECT * FROM Clientes")
        resultados = cursor.fetchall()
        for cliente in resultados:
            print(cliente)
except Exception as e:
    print(f"Error: {e}")
finally:
    conexion.close()
