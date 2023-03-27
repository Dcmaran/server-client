import socket

# Configurações do servidor
HOST = ''  # IP local
PORT = 5000  # Porta de escuta
BUFFER_SIZE = 32

# Cria um socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associa o socket a um endereço e porta
server_socket.bind((HOST, PORT))

# Escuta conexões
server_socket.listen()

print('Servidor iniciado em', (HOST, PORT))

# Espera por conexões
while True:
    # Aceita a conexão do cliente
    client_socket, address = server_socket.accept()
    print('Conexão estabelecida com', address)

    # Recebe mensagens do cliente
    while True:
        data = client_socket.recv(BUFFER_SIZE)

        if not data:
            break

        # Confirma recebimento da mensagem
        client_socket.sendall(b'ACK')

        print('Mensagem recebida:', data.decode())

    # Fecha a conexão com o cliente
    client_socket.close()
    print('Conexão fechada com', address)
