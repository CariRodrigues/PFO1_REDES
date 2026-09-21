import socket
import sqlite3
from datetime import datetime

#Función que prepara la base de datos
def inicializar_db():
    conexion_db = None
    try:
        conexion_db = sqlite3.connect('chat.db')
        cursor = conexion_db.cursor()
        #tabla p/ guardar los msj
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contenido TEXT,
            fecha_envio TEXT,
            ip_cliente TEXT)
        ''')
        conexion_db.commit()
        return True
    except sqlite3.Error:
        print("Ocurrió un error al inicializar la DB")
        return False
    finally:
        if conexion_db is not None:
            conexion_db.close()

#función que almacena los mensajes en la base (en la tabla creada)
def guardar_mensaje(contenido, fecha_envio, ip_cliente):
        conexion_db = None
        try:
            conexion_db = sqlite3.connect('chat.db')
            cursor = conexion_db.cursor()

            cursor.execute('''
                INSERT INTO mensajes (contenido, fecha_envio, ip_cliente)
                VALUES (?, ?, ?) 
            ''', (contenido, fecha_envio, ip_cliente))

            conexion_db.commit()
            
        except sqlite3.Error:
            print("Ocurrió un error al guardar el mensaje en la base de datos")
        finally:
            if conexion_db is not None:
                conexion_db.close()

#configuración del socket (TCP/IP)
def inicializar_servidor():
    #creación del socket que espera conexiones con algún cliente
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #espera la conexión de un cliente
    try:
        servidor.bind(('127.0.0.1' , 5000)) 
    except OSError:
        print("No se pudo iniciar el servidor porque el puerto está ocupado")
        return None

    servidor.listen()
    print("servidor escuchando en localhost 5000")
    return servidor

#acepta la conexión con el cliente, recibe mensajes y responde
def aceptar_conexion(servidor):
    #conexion (socket de comunicación con el cliente)
    conexion, direccion = servidor.accept() 
    print("cliente conectado", direccion)

    while True: 
            #recibe los datos
            datos = conexion.recv(1024) 
            if datos == b'':
                break
    
            datos = datos.decode("utf-8")
            fecha_hora = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            guardar_mensaje(datos, fecha_hora, direccion[0])
    
            print(f"Mensaje recibido:{datos}, {fecha_hora}")
    
            respuesta = f"Mensaje recibido: {fecha_hora}"    
            conexion.sendall(respuesta.encode('utf-8')) #envía respuesta

    conexion.close() #cerramos el socket con ese cliente


def main():

    db_ok = inicializar_db()

    if not db_ok:
        print("Error al inicializar la base de datos")
        return
        
    servidor = inicializar_servidor()
    if servidor is None:
        return

    aceptar_conexion(servidor)
    
if __name__ == "__main__":
    main()

