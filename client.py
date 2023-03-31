import socket
import random
import hashlib

# Configurações do cliente
HOST = '127.0.0.1'  # IP do servidor
PORT = 5000  # Porta do servidor
BUFFER_SIZE = 1024

seq_num = 0

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
        
        msg_id = random.randint(1000,9999)

        # Calcula a soma de verificação da mensagem
        hash_object = hashlib.sha256(message.encode())
        checksum = hash_object.hexdigest()

        # Adiciona o número de sequência à mensagem
        message = f"{msg_id},{seq_num},{message},{checksum}"

        # Envia a mensagem
        client_socket.sendall(message.encode())

        # Recebe a confirmação do servidor
        data = client_socket.recv(BUFFER_SIZE)

        # Converte a confirmação para inteiro
        received_msg = data.decode()

        # Verifica se o número de sequência recebido corresponde ao esperado
        if received_msg == 'ACK':
            print('Confirmação recebida:', data.decode())
            seq_num += 1
            
        elif received_msg == 'NACK':
            print('Pacote não reconhecido')
            seq_num += 1


# Fecha a conexão com o servidor
client_socket.close()
print('Conexão fechada')
