import pymysql
import pandas as pd
from sqlalchemy import create_engine

# Crear el motor de conexión SQLAlchemy
engine = create_engine('mysql+pymysql://uzzi1lzjkhuq2y92:TWwLvF3658qNHnmTU7KX@bo2hc4epacbxc16ou5of-mysql.services.clever-cloud.com:3306/bo2hc4epacbxc16ou5of')

# Cargar datos en un DataFrame
clientes = pd.read_sql('SELECT * FROM Clientes', engine)

# Limpiar la columna 'correo'
clientes['correo'] = clientes['correo'].str.replace('@@', '@', regex=False)
clientes['correo'] = clientes['correo'].apply(lambda x: x if '@' in x and '.' in x else None)

# Limpiar la columna 'telefono'
clientes['telefono'] = clientes['telefono'].str.replace('[^0-9]', '', regex=True)

# Conectar a la base de datos usando pymysql para actualizar los valores limpios
conexion = pymysql.connect(
    host='bo2hc4epacbxc16ou5of-mysql.services.clever-cloud.com',
    user='uzzi1lzjkhuq2y92',
    password='TWwLvF3658qNHnmTU7KX',
    database='bo2hc4epacbxc16ou5of',
    port=3306,
    cursorclass=pymysql.cursors.DictCursor
)

# Actualizar la base de datos con los datos limpios
try:
    for index, row in clientes.iterrows():
        with conexion.cursor() as cursor:
            cursor.execute(
                "UPDATE Clientes SET correo = %s, telefono = %s WHERE id_cliente = %s",
                (row['correo'], row['telefono'], row['id_cliente'])
            )
    conexion.commit()
except Exception as e:
    print(f"Error: {e}")
finally:
    conexion.close()
