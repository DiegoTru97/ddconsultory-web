import os
import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def inicio():
    # Carga tu página principal
    return render_template('index.html')


@app.route('/enviar_contacto', methods=['POST'])
def contacto():
    try:
        # Extraemos los datos que nos envía el JavaScript
        datos = request.get_json()
        nombre = datos.get('nombre')
        servicio = datos.get('servicio')
        mensaje = datos.get('mensaje')

        # 1. Validación básica de seguridad (evita enviar correos vacíos)
        if not nombre or not mensaje:
            return jsonify({"status": "error", "message": "Datos incompletos"}), 400

        # 2. Configuración de credenciales de correo desde las variables de Render
        # NUNCA se ponen las contraseñas directamente en el código por seguridad.
        remitente = os.environ.get('EMAIL_USER')
        password = os.environ.get('EMAIL_PASS')
        destinatario = 'diegotru1230@gmail.com'

        # Si aún no configuras las contraseñas en Render, solo imprime en consola
        if not remitente or not password:
            print(f"MENSAJE SIMULADO (Faltan credenciales): De {nombre} - {mensaje}")
            return jsonify({"status": "success", "message": "Simulado correctamente"})

        # 3. Construcción del correo electrónico
        msg = EmailMessage()
        msg['Subject'] = f'Nueva solicitud en DDConsultory: {servicio}'
        msg['From'] = remitente
        msg['To'] = destinatario

        cuerpo_correo = f"""
        ¡Hola Diego! Tienes un nuevo mensaje desde tu sitio web DDConsultory.

        Detalles del cliente:
        ----------------------------------------
        Nombre: {nombre}
        Servicio de interés: {servicio}

        Mensaje del cliente:
        ----------------------------------------
        {mensaje}
        """
        msg.set_content(cuerpo_correo)

        # 4. Envío seguro del correo usando el servidor de Gmail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(remitente, password)
            smtp.send_message(msg)

        print("Correo enviado exitosamente.")
        return jsonify({"status": "success", "message": "Mensaje recibido correctamente"})

    except Exception as e:
        print(f"Error enviando correo: {e}")
        return jsonify({"status": "error", "message": "Hubo un problema al procesar la solicitud"}), 500


if __name__ == '__main__':
    print("Iniciando el servidor...")
    app.run(debug=True, port=5000)