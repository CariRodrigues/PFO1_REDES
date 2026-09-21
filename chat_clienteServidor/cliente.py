import socket
#creación del socket del lado del cliente
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#cliente se conecta al servidor indicado, en puerto 5000
cliente.connect(('127.0.0.1', 5000))

mensaje = ""
while mensaje != "éxito":
    mensaje = input("Ingrese un mensaje: ")

    if mensaje == "éxito":
        break


    mensajebytes = mensaje.encode('utf-8')
    cliente.send(mensajebytes)

    respuesta = cliente.recv(1024).decode("utf-8")
    print(respuesta)

    
