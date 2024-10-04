import socket
import os
import pickle
import time
import threading

hostname = socket.gethostname()
direccion_ip = socket.gethostbyname(hostname)

os.system("clear")
print("Made and developed by gneval9")
print("(27-08-2024)")
print("Ver. 1.0")
time.sleep(2)

# Lista para almacenar mensajes
messages = []
clients = []  # Lista de clientes conectados
lock = threading.Lock()  # Lock para sincronizar el acceso a mensajes

def connect():
    os.system("clear")
    global port, cliente_socket
    host_to_connect = input("Introduzca la direccion IP del ordenador con el que quieres comunicarte: ")
    port = int(input("Introduzca el puerto al que desea conectarse: "))
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        print("Conectando...")
        time.sleep(5)
        cliente_socket.connect((host_to_connect, port))
        print("Conexión establecida")
    except OSError as e:
        print(f"No se ha podido conectar: {e}")
        time.sleep(3)
        init()
    
    # Enviar el nombre de usuario al servidor
    datos_a_enviar = pickle.dumps(usr_name)
    cliente_socket.sendall(datos_a_enviar)
    
    # Iniciar hilos para recibir y enviar mensajes
    threading.Thread(target=recibir_mensajes).start()
    threading.Thread(target=enviar_mensajes).start()

def enviar_mensajes():
    print("Conectado")
    print("Introduzca su mensaje aqui (o 'exit' para salir): ")
    while True:
        mensaje = input()
        if mensaje.lower() == 'exit':
            break
        elif mensaje == "!server_data":
            print(f"Datos del servidor: IP = {direccion_ip}, Puerto = {port}")
            continue
        
        datos_a_enviar = pickle.dumps((usr_name, mensaje))
        cliente_socket.sendall(datos_a_enviar)

        with lock:
            messages.append(f"Tú: {mensaje}")
            mostrar_mensajes()

def recibir_mensajes():
    while True:
        try:
            datos_serializados = cliente_socket.recv(1024)
            if datos_serializados:
                variable1_recibida, variable2_recibida = pickle.loads(datos_serializados)
                mensaje_recibido = f"{variable1_recibida}: {variable2_recibida}"
                with lock:
                    messages.append(mensaje_recibido)
                    mostrar_mensajes()
        except Exception as e:
            print(f"Error al recibir el mensaje: {e}")
            break

def host():
    os.system("clear")
    global port, servidor_socket
    port = int(input("Indique el puerto de escucha: "))
    os.system("clear")
    print(f"Servidor actual: {direccion_ip}:{port}")
    print("Servidor a la espera de conexiones entrantes...")
    print("-----------------------------------------------")
    
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.bind(('0.0.0.0', port))
    servidor_socket.listen()

    while True:
        cliente_socket, address = servidor_socket.accept()
        clients.append(cliente_socket)
        # Recibir nombre de usuario del cliente
        datos_serializados = cliente_socket.recv(1024)
        remote_usr_name = pickle.loads(datos_serializados)
        print(f"Conexion establecida con {remote_usr_name} ({address})")
        
        # Iniciar hilos para recibir y enviar mensajes
        threading.Thread(target=recibir_mensajes_host, args=(cliente_socket,)).start()
        threading.Thread(target=enviar_mensajes_host, args=(cliente_socket, remote_usr_name)).start()

def enviar_mensajes_host(cliente_socket, remote_usr_name):
    print("Introduzca su mensaje aqui (o 'exit' para salir): ")
    while True:
        mensaje = input()
        if mensaje != "":
            if mensaje.lower() == 'exit':
                break
            elif mensaje == "!server_data":
                print(f"Datos del servidor: IP = {direccion_ip}, Puerto = {port}")
                continue
            
            datos_a_enviar = pickle.dumps((usr_name, mensaje))
            cliente_socket.sendall(datos_a_enviar)

            with lock:
                messages.append(f"Tú: {mensaje}")
                mostrar_mensajes()

def recibir_mensajes_host(cliente_socket):
    while True:
        try:
            datos_serializados = cliente_socket.recv(1024)
            if datos_serializados:
                variable1_recibida, variable2_recibida = pickle.loads(datos_serializados)
                mensaje_recibido = f"{variable1_recibida}: {variable2_recibida}"
                with lock:
                    messages.append(mensaje_recibido)
                    mostrar_mensajes()
        except Exception as e:
            print(f"{remote_usr_name} se ha desconectado") # type: ignore
            break

def mostrar_mensajes():
    os.system("clear")
    for msg in messages:
        print(msg)

def init():
    os.system("clear")
    
    def usr_Name():
        global usr_name
        usr_name = input("Antes de comenzar introduzca su nombre: ")
    usr_Name()
    if usr_name == "":
        print("Nombre no valido, intetnelo de nuevo")
        time.sleep(2)
        os.system("clear")
        usr_Name()
    
    os.system("clear")
    print("Introduzca 'host' para crear un chat o 'connect' para conectarse a un chat creado")
    print("Pulse [Enter] sin introducir nada para cambiar el nombre")
    mode = input()
    
    if mode == "host":
        host()
    elif mode == "connect":
        connect()
    elif mode != "host" or "connect" and mode == "":
        init()
    else:
        print("Opción no válida")
        init()

init()
