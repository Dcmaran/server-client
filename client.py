import socket
import sys
import random
import hashlib
import select

#CLIENTE REAL OFICIAL

# Configurações do cliente
HOST = '127.0.0.1'  # IP do servidor
PORT = 5000  # Porta do servidor
BUFFER_SIZE = 1024

TIMER =  7
MAX_ATTEMPTS = 3

validator = 0
attempt = 0

cont_pack = 0

seq_num = 0

def isParallel(msg):
    return '|' in msg

def send_message(msg):
    msg_id = random.randint(1000, 9999)

    # Calcula a soma de verificação da mensagem
    hash_object = hashlib.sha256(msg.encode())
    checksum = hash_object.hexdigest()

    # Adiciona o número de sequência à mensagem
    msg = f"{msg_id},{seq_num},{msg},{checksum}"

    return msg


# Cria um socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET is the Internet address family for IPv4. SOCK_STREAM is the socket type for TCP

# Conecta-se ao servidor
client_socket.connect((HOST, PORT))
print('Conectado ao servidor em', (HOST, PORT))

# Envia mensagens para o servidor
with client_socket:
    while True:
        try:
            
            print(F"Digite a mensagem (você tem {TIMER} segundos): ", end='', flush=True)
            ready, _, _ = select.select([sys.stdin], [], [], TIMER)  # Timeout de 5 segundos

            if ready:
                message = sys.stdin.readline().strip()

                if message == 'sair':
                   print("\nConexão encerrada pelo usuário.")
                   break

                if isParallel(message):
                    message = message.split('|')

                    for i in message:
                        if i == 'sair':
                            print("\nConexão encerrada pelo usuário.")
                            exit(1)

                        mensagem = send_message(i)

                        seq_num = seq_num - attempt

                        # Envia a mensagem
                        client_socket.sendall(mensagem.encode())

                        # Recebe a confirmação do servidor
                        data = client_socket.recv(BUFFER_SIZE)

                        # Converte a confirmação para inteiro
                        received_msg = data.decode()

                        seq_num += 1

                        validator += 1
                            
                        # Verifica se o número de sequência recebido corresponde ao esperado
                        if received_msg == 'ACK':
                            print(f'Confirmação individual pacote {seq_num} recebida:', data.decode())
                            
                            if attempt == 0:
                                print('Todos os pacotes enviados')

                            if attempt == 1:
                                print('Reenviar 1 pacote')
                                attempt-=1

                            if attempt == 2:
                                print('Reenviar 2 pacotes')  
                                attempt-=1

                            cont_pack += 1

                            validator = 0

                        if cont_pack == len(message):
                            print('Confirmacao do lote recebida: ACK')



                else:
                    mensagem = send_message(message)

                    # Envia a mensagem
                    client_socket.sendall(mensagem.encode())

                    # Recebe a confirmação do servidor
                    data = client_socket.recv(BUFFER_SIZE)

                    # Converte a confirmação para inteiro
                    received_msg = data.decode()

                    # Verifica se o número de sequência recebido corresponde ao esperado
                    if received_msg == 'ACK':
                        print('Confirmação recebida:', data.decode())

                        if attempt == 0:
                            print('Todos os pacotes enviados')
                            seq_num += 1

                        if attempt == 1:
                            print('Reenviar 1 pacote')
                            attempt-=1

                        if attempt == 2:
                            print('Reenviar 2 pacotes')  
                            attempt-=1

                    if received_msg == 'NACK':
                        print("Pacote com falha de integridade", data.decode())
                        print('Reenviar 1 pacote')


            else:
                print(f"\nErro: você não digitou uma mensagem em {TIMER} segundos.")
                print("Pacote perdido")
                attempt += 1
                print(attempt)
                seq_num += 1

                if attempt == MAX_ATTEMPTS:
                    print('Não foi possível enviar a mensagem. Encerrando a conexão...')
                    break

                continue
                

        except KeyboardInterrupt:
            print("\nConexão encerrada pelo usuário.")
            break

# Fecha a conexão com o servidor
client_socket.close()
print('Conexão fechada')