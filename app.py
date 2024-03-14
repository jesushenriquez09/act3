from flask import Flask, request, jsonify
import pymysql

# Configuramos la conexión a la base de datos
db_config = {
    'host': 'localhost:3306',
    'user': 'root',
    'password': '',
    'database': 'crud',
}

# Creamos una instancia de la aplicación Flask
app = Flask(__name__)

# Definimos una función para ejecutar consultas SQL
def execute_query(query, params=None):
    # Iniciamos la conexión y el cursor
    conn = None
    cursor = None
    try:
        # Conectamos a la base de datos
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        # Ejecutamos la consulta
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        # Hacemos commit de la transacción
        conn.commit()
        # Obtenemos los resultados
        result = cursor.fetchall()
        return result
    except Exception as e:
        # Imprimimos el error si algo sale mal
        print(f"Error al ejecutar la consulta: {e}")
        return None
    finally:
        # Cerramos el cursor y la conexión
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Definimos la ruta para manipular datos de usuarios
@app.route('/usuarios', methods=['GET', 'POST', 'PUT', 'DELETE'])
def usuarios():
    if request.method == 'GET':
        # Para las solicitudes GET, seleccionamos todos los usuarios
        query = "SELECT * FROM usuarios"
        result = execute_query(query)
        return jsonify(result)
    elif request.method == 'POST':
        # Para las solicitudes POST, creamos un nuevo usuario
        nombre = request.json.get('nombre')
        edad = request.json.get('edad')
        if nombre and edad:
            query = "INSERT INTO usuarios (nombre, edad) VALUES (%s, %s)"
            execute_query(query, (nombre, edad))
            return 'Usuario creado exitosamente', 201
        else:
            return 'Datos de entrada inválidos', 400
    elif request.method == 'PUT':
        # Para las solicitudes PUT, actualizamos un usuario existente
        id = request.json.get('id')
        nombre = request.json.get('nombre')
        edad = request.json.get('edad')
        if id and nombre and edad:
            query = "UPDATE usuarios SET nombre = %s, edad = %s WHERE id = %s"
            execute_query(query, (nombre, edad, id))
            return 'Usuario actualizado exitosamente', 200
        else:
            return 'Datos de entrada inválidos', 400
    elif request.method == 'DELETE':
        # Para las solicitudes DELETE, eliminamos un usuario
        id = request.json.get('id')
        if id:
            query = "DELETE FROM usuarios WHERE id = %s"
            execute_query(query, (id,))
            return 'Usuario eliminado exitosamente', 200
        else:
            return 'Datos de entrada inválidos', 400

# Definimos la ruta para manipular datos de carros
@app.route('/carros', methods=['GET', 'POST', 'PUT', 'DELETE'])
def carros():
    if request.method == 'GET':
        # Para las solicitudes GET, seleccionamos todos los carros
        query = "SELECT * FROM carros"
        result = execute_query(query)
        return jsonify(result)
    elif request.method == 'POST':
        # Para las solicitudes POST, creamos un nuevo carro
        marca = request.json.get('marca')
        modelo = request.json.get('modelo')
        if marca and modelo:
            query = "INSERT INTO carros (marca, modelo) VALUES (%s, %s)"
            execute_query(query, (marca, modelo))
            return 'Carro creado exitosamente', 201
        else:
            return 'Datos de entrada inválidos', 400
    elif request.method == 'PUT':
        # Para las solicitudes PUT, actualizamos un carro existente
        id = request.json.get('id')
        marca = request.json.get('marca')
        modelo = request.json.get('modelo')
        if id and marca and modelo:
            query = "UPDATE carros SET marca = %s, modelo = %s WHERE id = %s"
            execute_query(query, (marca, modelo, id))
            return 'Carro actualizado exitosamente', 200
        else:
            return 'Datos de entrada inválidos', 400
    elif request.method == 'DELETE':
        # Para las solicitudes DELETE, eliminamos un carro
        id = request.json.get('id')
        if id:
            query = "DELETE FROM carros WHERE id = %s"
            execute_query(query, (id,))
            return 'Carro eliminado exitosamente', 200
        else:
            return 'Datos de entrada inválidos', 400

# Iniciamos la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True, port=5000)