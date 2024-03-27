import threading
import socket
import os
import pickle
import time
import keyboard as kb

hostname = socket.gethostname()
direccion_ip = socket.gethostbyname(hostname)

os.system("clear")
print("Made and developed by gneval9")
print("(19-03-2024)")
print("Ver. Beta")
time.sleep(2)
os.system("clear")






def connect():

    host_to_connect = input("Introduzca la direccion IP del ordenador con el quieres comunicarte: ")
    # Crear un socket y conectarlo al servidor
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect((host_to_connect, 8800))
    espera_de_datos()



def chat():
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        # Datos a enviar
        mensaje = input("Introduzca su mensaje aqui: ")
        datos_a_enviar = (ip_address, mensaje)

        # Serializar los datos utilizando pickle y enviarlos al servidor
        datos_serializados = pickle.dumps(datos_a_enviar)
        cliente_socket.sendall(datos_serializados)

        espera_de_datos()




def host():
    print(f"Direccion IP del servidor actual: {direccion_ip}")
    print("Servidor a la espera de datos entrantes...")
    print("------------------------------------------")
    espera_de_datos()









def espera_de_datos():
    # Crear un socket y esperar por la conexión
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.bind((direccion_ip,8800))
    servidor_socket.listen(1)
    hilo = threading.Thread(target=cambio_a_chat)
    hilo.start()
    

    while True:
        
        cliente_socket, address = servidor_socket.accept()
        
        # Recibir los datos serializados y deserializarlos
        datos_serializados = cliente_socket.recv(1024)
        datos_recibidos = pickle.loads(datos_serializados)

        # Procesar los datos recibidos
        variable1_recibida, variable2_recibida = datos_recibidos
        print()
        print("IP del usuario:", variable1_recibida)
        print("Mensaje:", variable2_recibida)

def cambio_a_chat():
    while True:
        if kb.is_pressed("t"):
            os.system("clear")
            chat()



def init():
    mode = input("Introduzca 'host' para crear un chat o 'connect' para conectarse a un chat creado: ")

    if mode == "host":
        host()

    elif mode == "connect":
        connect()

    else:
        init()




init()