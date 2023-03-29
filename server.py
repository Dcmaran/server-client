import sys
import socket

# Configurações do servidor
HOST = ''  # IP local
PORT = 5000  # Porta de escuta
BUFFER_SIZE = 1024

# Cria um socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associa o socket a um endereço e porta
server_socket.bind((HOST, PORT)) #.bind() method is used to associate the socket with a specific network 

# Escuta conexões
server_socket.listen()  #.listen() enables a server to accept connections
print('Servidor iniciado em', (HOST, PORT))

# Aceita a conexão do cliente
client_socket, address = server_socket.accept() #The .accept() method blocks execution and waits for an incoming connection.
#it returns a new socket object representing the connection(client_socket) and a tuple holding the address of the client(address)
#A socket function or method that temporarily suspends your application is a blocking call.
#For example, .accept(), .connect(), .send(), and .recv() block, meaning they don’t return immediately. 
# Blocking calls have to wait on system calls (I/O) to complete before they can return a value.

client_socket.settimeout(5)

print('Conexão estabelecida com', address)

# Espera por conexões
with client_socket:

    # Recebe mensagens do cliente
    while True:
        try:
            data = client_socket.recv(BUFFER_SIZE)

            # Confirma recebimento da mensagem
            client_socket.sendall(b'ACK')
            
            print('Mensagem recebida:', data.decode())

            if not data:
                break
        except:
            print("PACOTE PERDIDO")
            

    # Fecha a conexão com o cliente
    client_socket.close()
    print('Conexão fechada com', address)
