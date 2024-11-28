from flask import Flask, render_template
from flask_mysqldb import MySQL
from datetime import datetime

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
def mostrar_graficas():
    try:
        cursor = mysql.connection.cursor()

        # Obtener datos para los gráficos
        cursor.execute("SELECT nombre, precio FROM Productos")
        productos = cursor.fetchall()
        nombres_productos = [producto['nombre'] for producto in productos]
        precios_productos = [float(producto['precio']) for producto in productos]

        cursor.execute("SELECT fecha_venta, cantidad FROM Ventas")
        ventas = cursor.fetchall()
        
        fechas_ventas = []
        for venta in ventas:
            if isinstance(venta['fecha_venta'], str):
                try:
                    fecha = datetime.strptime(venta['fecha_venta'], '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    fecha = None
            else:
                fecha = venta['fecha_venta']

            if fecha:
                fechas_ventas.append(fecha.strftime('%Y-%m-%d'))
            else:
                fechas_ventas.append('N/A')
        
        cantidades_ventas = [float(venta['cantidad']) for venta in ventas]

        cursor.execute("SELECT nombre FROM Clientes")
        clientes = cursor.fetchall()
        nombres_clientes = [cliente['nombre'] for cliente in clientes]

        # Gráfica adicional: Total de Ventas por Cliente
        cursor.execute("SELECT c.nombre, COUNT(v.id_venta) as total_ventas FROM Clientes c LEFT JOIN Ventas_Clientes vc ON c.id_cliente = vc.id_cliente LEFT JOIN Ventas v ON vc.id_venta = v.id_venta GROUP BY c.nombre")
        ventas_clientes = cursor.fetchall()
        nombres_clientes_ventas = [item['nombre'] for item in ventas_clientes]
        total_ventas_clientes = [item['total_ventas'] for item in ventas_clientes]

        # Gráfica adicional: Productos por Categoría
        cursor.execute("SELECT categoria, COUNT(*) as total_productos FROM Productos GROUP BY categoria")
        productos_categoria = cursor.fetchall()
        categorias_productos = [item['categoria'] for item in productos_categoria]
        total_productos_categoria = [item['total_productos'] for item in productos_categoria]

        cursor.close()
        return render_template('index.html', 
                               nombres_productos=nombres_productos, precios_productos=precios_productos,
                               fechas_ventas=fechas_ventas, cantidades_ventas=cantidades_ventas,
                               nombres_clientes=nombres_clientes,
                               nombres_clientes_ventas=nombres_clientes_ventas, total_ventas_clientes=total_ventas_clientes,
                               categorias_productos=categorias_productos, total_productos_categoria=total_productos_categoria)
    except Exception as e:
        return f"Error al conectar con la base de datos: {e}"

if __name__ == '__main__':
    app.run(debug=True)
