import socket

# Configurações do cliente
HOST = '127.0.0.1'  # IP do servidor
PORT = 5000  # Porta do servidor
BUFFER_SIZE = 1024

# Cria um socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET is the Internet address family for IPv4. SOCK_STREAM is the socket type for TCP

# Conecta-se ao servidor
client_socket.connect((HOST, PORT))
print('Conectado ao servidor em', (HOST, PORT))

# Envia mensagens para o servidor
with client_socket:

    while True:
        # Gera uma mensagem aleatória
        message = input("Digite a mensagem: ")

        if message == 'sair':
            break

        # Envia a mensagem
        client_socket.sendall(message.encode())

        # Espera um tempo aleatório para simular perda de mensagem
        #time.sleep(random.uniform(0, 1))

        # Recebe a confirmação do servidor
        data = client_socket.recv(BUFFER_SIZE)

        print('Confirmação recebida:', data.decode())

# Fecha a conexão com o servidor
client_socket.close()
print('Conexão fechada')
