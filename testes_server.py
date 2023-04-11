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
server_socket.bind((HOST, PORT)) #.bind() method is used to associate the socket with a specific network 

# Escuta conexões
server_socket.listen()  #.listen() enables a server to accept connections
print('Servidor iniciado em', (HOST, PORT))

# Espera por conexões
while True:
    try:
        # Aceita a conexão do cliente
        client_socket, address = server_socket.accept() #The .accept() method blocks execution and waits for an incoming connection.
        #it returns a new socket object representing the connection(client_socket) and a tuple holding the address of the client(address)
        #A socket function or method that temporarily suspends your application is a blocking call.

        print('Conexão estabelecida com', address)

        # Recebe mensagens do cliente
        with client_socket:
            while True:
                
                data = client_socket.recv(BUFFER_SIZE)

                if not data:
                    break

                # Converte a lista de mensagens para uma lista Python
                messages = data.decode().split('|')
                
                # Processa cada mensagem individualmente
                for msg in messages:
                    # Separa o número de sequência e a mensagem
                    msg_id, received_seq_num, message, checksum = msg.split(',')

                    # Converte o número de sequência para inteiro
                    received_seq_num = int(received_seq_num)

                    # Calcula a soma de verificação da mensagem
                    hash_object = hashlib.sha256(message.encode())
                    calc_checksum = hash_object.hexdigest()

                    print('Mensagem recebida:', msg)

                    if checksum != calc_checksum:
                        print('Pacote fora de ordem ou inválido')

                    #Verifica se o número de sequência é esperado
                    if received_seq_num != seq_num:
                        print('Pacote fora de ordem ou duplicado')      

                    # Confirma recebimento da mensagem
                    client_socket.sendall(b'ACK')

                    # Incrementa o número de sequência
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