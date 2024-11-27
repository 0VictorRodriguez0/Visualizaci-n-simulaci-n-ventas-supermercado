import pymysql
import pandas as pd
from sqlalchemy import create_engine

# Crear el motor de conexión SQLAlchemy
engine = create_engine('mysql+pymysql://uzzi1lzjkhuq2y92:TWwLvF3658qNHnmTU7KX@bo2hc4epacbxc16ou5of-mysql.services.clever-cloud.com:3306/bo2hc4epacbxc16ou5of')

# Cargar datos en un DataFrame
productos = pd.read_sql('SELECT * FROM Productos', engine)

# Limpiar la columna 'precio'
productos['precio'] = productos['precio'].replace({'un dólar': '1.00', 'dos dolares': '2.00', 'dos y medio': '2.50', 'cuatro dolares': '4.00', '15 dolares': '15.00'}, regex=True)
productos['precio'] = productos['precio'].str.replace('[^0-9.]', '', regex=True)
productos['precio'] = pd.to_numeric(productos['precio'], errors='coerce').fillna(0.0)

# Limpiar la columna 'fecha_expiracion'
productos['fecha_expiracion'] = pd.to_datetime(productos['fecha_expiracion'], errors='coerce').fillna(pd.NaT)

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
    for index, row in productos.iterrows():
        with conexion.cursor() as cursor:
            cursor.execute(
                "UPDATE Productos SET precio = %s, fecha_expiracion = %s WHERE id_producto = %s",
                (float(row['precio']), row['fecha_expiracion'], row['id_producto'])
            )
    conexion.commit()
except Exception as e:
    print(f"Error: {e}")
finally:
    conexion.close()
