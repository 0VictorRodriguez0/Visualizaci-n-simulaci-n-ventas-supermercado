from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de la conexión a la base de datos
app.config['MYSQL_HOST'] = 'bo2hc4epacbxc16ou5of-mysql.services.clever-cloud.com'
app.config['MYSQL_USER'] = 'uzzi1lzjkhuq2y92'
app.config['MYSQL_PASSWORD'] = 'TWwLvF3658qNHnmTU7KX'
app.config['MYSQL_DB'] = 'bo2hc4epacbxc16ou5of'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # Para obtener los resultados como diccionarios

mysql = MySQL(app)

@app.route('/')
def mostrar_tablas():
    try:
        cursor = mysql.connection.cursor()
        # tablas = ['Productos', 'Ventas', 'Clientes']
        tablas = ['Productos', 'Ventas', 'Clientes', 'Ventas_Clientes']
        datos_tablas = {}

        for tabla in tablas:
            # Obtener las columnas de la tabla
            cursor.execute(f"DESCRIBE {tabla}")
            columnas = cursor.fetchall()
            # Obtener las filas de la tabla
            cursor.execute(f"SELECT * FROM {tabla}")
            filas = cursor.fetchall()
            datos_tablas[tabla] = {'columnas': columnas, 'filas': filas}
        print(datos_tablas)

        cursor.close()
        return render_template('index.html', datos_tablas=datos_tablas)
    except Exception as e:
        return f"Error al conectar con la base de datos: {e}"

if __name__ == '__main__':
    app.run(debug=True)
