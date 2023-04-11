import sys
import socket
import hashlib

# Configurações do servidor
HOST = ''  # IP local
PORT = 5000  # Porta de escuta
BUFFER_SIZE = 1024

seq_num = 0

# Cria um socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associa o socket a um endereço e porta
server_socket.bind((HOST, PORT))

# Escuta conexões
server_socket.listen()
print('Servidor iniciado em', (HOST, PORT))

# Espera por conexões
while True:
    try:
        # Aceita a conexão do cliente
        client_socket, address = server_socket.accept()
        print('Conexão estabelecida com', address)

        # Recebe mensagens do cliente
        with client_socket:
            while True:

                data = client_socket.recv(BUFFER_SIZE)

                if not data:
                    break

                # Separa o número de sequência e a mensagem
                msg_id, received_seq_num, message, checksum = data.decode().split(',')

                # Converte o número de sequência para inteiro
                received_seq_num = int(received_seq_num)

                # Calcula a soma de verificação da mensagem
                hash_object = hashlib.sha256(message.encode())
                calc_checksum = hash_object.hexdigest()

                print('Mensagem recebida:', data.decode())

                print(seq_num)
                print(received_seq_num)

                if received_seq_num != seq_num or checksum != calc_checksum:
                    print('Pacote fora de ordem, inválido ou duplicado')
                    client_socket.sendall(b'NAK')
                else:
                    client_socket.sendall(b'ACK')
                    seq_num += 1

    except ConnectionResetError:
        print('Conexão encerrada abruptamente pelo cliente')
        break

    except KeyboardInterrupt:
            print("\nServidor encerrado pelo usuário.")
            break

    # Fecha a conexão com o cliente
    client_socket.close()
    print('Conexão fechada com', address)
    seq_num = 0