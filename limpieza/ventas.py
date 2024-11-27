import pymysql
import pandas as pd
from sqlalchemy import create_engine

# Crear el motor de conexión SQLAlchemy
engine = create_engine('mysql+pymysql://uzzi1lzjkhuq2y92:TWwLvF3658qNHnmTU7KX@bo2hc4epacbxc16ou5of-mysql.services.clever-cloud.com:3306/bo2hc4epacbxc16ou5of')

# Cargar datos en un DataFrame
ventas = pd.read_sql('SELECT * FROM Ventas', engine)


# Limpiar la columna 'cantidad'
ventas['cantidad'] = ventas['cantidad'].replace({'cinco': '5', 'cuatro': '4', 'uno': '1', 'dos': '2'}, regex=True)
ventas['cantidad'] = pd.to_numeric(ventas['cantidad'], errors='coerce').fillna(0.0)

# Limpiar la columna 'fecha_venta'
ventas['fecha_venta'] = pd.to_datetime(ventas['fecha_venta'], errors='coerce').fillna(pd.NaT)

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
    for index, row in ventas.iterrows():
        with conexion.cursor() as cursor:
            cursor.execute(
                "UPDATE Ventas SET cantidad = %s, fecha_venta = %s WHERE id_venta = %s",
                (row['cantidad'], row['fecha_venta'], row['id_venta'])
            )
    conexion.commit()
except Exception as e:
    print(f"Error: {e}")
finally:
    conexion.close()