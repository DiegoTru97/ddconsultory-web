import os
import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def inicio():
    return render_template('index.html')


@app.route('/enviar_contacto', methods=['POST'])
def contacto():
    print("--- NUEVA SOLICITUD DE CONTACTO ---")
    try:
        datos = request.get_json()
        nombre = datos.get('nombre')
        servicio = datos.get('servicio')
        mensaje = datos.get('mensaje')

        if not nombre or not mensaje:
            print("Error: Datos incompletos enviados por el cliente.")
            return jsonify({"status": "error", "message": "Datos incompletos"}), 400

        remitente = os.environ.get('EMAIL_USER')
        password = os.environ.get('EMAIL_PASS')
        destinatario = 'diegotru1230@gmail.com'

        if not remitente or not password:
            print(f"MENSAJE SIMULADO (Faltan credenciales en Render): De {nombre} - {mensaje}")
            return jsonify({"status": "success", "message": "Simulado correctamente. (Faltan credenciales)"}), 200

        print(f"Preparando correo de {nombre} usando la cuenta {remitente}...")

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

        print("Intentando conectar con smtp.gmail.com por el puerto 465 (SSL)...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10) as smtp:
            print("Conexión SMTP exitosa. Intentando login...")
            smtp.login(remitente, password)
            print("Login exitoso. Enviando mensaje...")
            smtp.send_message(msg)
            print("¡Mensaje enviado al servidor de Gmail exitosamente!")

        return jsonify({"status": "success", "message": "Mensaje recibido correctamente"}), 200

    except smtplib.SMTPAuthenticationError as e:
        print(f"ERROR DE AUTENTICACIÓN (Contraseña incorrecta o bloqueada por Google): {e}")
        return jsonify(
            {"status": "error", "message": "Error de autenticación con el correo. Verifica las contraseñas."}), 500
    except smtplib.SMTPException as e:
        print(f"ERROR SMTP: {e}")
        return jsonify({"status": "error", "message": "Error de conexión con el servidor de correos."}), 500
    except Exception as e:
        print(f"ERROR GENERAL INESPERADO: {e}")
        return jsonify({"status": "error", "message": "Hubo un problema interno en el servidor."}), 500
    finally:
        print("--- FIN DE LA SOLICITUD ---")


if __name__ == '__main__':
    print("Iniciando el servidor en modo Debug...")
    app.run(debug=True, port=5000)