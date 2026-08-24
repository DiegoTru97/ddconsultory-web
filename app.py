from flask import Flask, render_template, request, jsonify

# Flask necesita saber dónde está el módulo principal
app = Flask(__name__)


@app.route('/')
def inicio():
    # Carga tu página principal
    return render_template('index.html')  # O index_alternativo.html si elegiste ese


# NUEVA RUTA: Esta parte recibe los datos del formulario de tu página web
@app.route('/enviar_contacto', methods=['POST'])
def contacto():
    # Extraemos los datos que nos envía el JavaScript
    datos = request.get_json()
    nombre = datos.get('nombre')
    servicio = datos.get('servicio')
    mensaje = datos.get('mensaje')

    # Por ahora, los imprimimos en la consola del servidor.
    # (¡En el futuro aquí pondremos el código para que te envíe un WhatsApp o un correo real!)
    print("----- NUEVO MENSAJE RECIBIDO -----")
    print(f"Nombre: {nombre}")
    print(f"Servicio: {servicio}")
    print(f"Mensaje: {mensaje}")
    print("----------------------------------")

    # Le respondemos a la página web que todo salió bien
    return jsonify({"status": "success", "message": "Mensaje recibido correctamente"})


if __name__ == '__main__':
    print("Iniciando el servidor...")
    app.run(debug=True, port=5000)