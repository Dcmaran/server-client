import socket
import sys
import random
import hashlib
import select
from concurrent.futures import ThreadPoolExecutor

# Configurações do cliente
HOST = '127.0.0.1'  # IP do servidor
PORT = 5000  # Porta do servidor
BUFFER_SIZE = 1024

def isParallel(msg):
    return '|' in msg

seq_num = 0

# Cria um socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET is the Internet address family for IPv4. SOCK_STREAM is the socket type for TCP

# Conecta-se ao servidor
client_socket.connect((HOST, PORT))
print('Conectado ao servidor em', (HOST, PORT))

# Envia mensagens para o servidor
with client_socket:
    while True:
        try:
            print("Digite a mensagem (você tem 5 segundos): ", end='', flush=True)
            ready, _, _ = select.select([sys.stdin], [], [], 5)  # Timeout de 5 segundos

            if ready:
                message = sys.stdin.readline().strip()
            else:
                print("\nErro: você não digitou uma mensagem em 5 segundos.")
                seq_num += 1
                continue

            if message == 'sair':
                print("\nConexão encerrada pelo usuário.")
                break

            msg_id = random.randint(1000, 9999)

            # Calcula a soma de verificação da mensagem
            hash_object = hashlib.sha256(message.encode())
            checksum = hash_object.hexdigest()

            # Adiciona o número de sequência à mensagem
            message = f"{msg_id},{seq_num},{message},{checksum}"
    
            # Separa as mensagens por "|"
            messages = message.split('|')

            # Envia as mensagens em paralelo usando threads
            with ThreadPoolExecutor(max_workers=len(messages)) as executor:
                results = []
                for msg in messages:
                    result = executor.submit(client_socket.sendall, msg.encode())
                    results.append(result)

                # Espera todas as threads terminarem
                for result in results:
                    result.result()
            

            # Recebe a confirmação do servidor
            data = client_socket.recv(BUFFER_SIZE)

            # Converte a confirmação para inteiro
            received_msg = data.decode()

            # Verifica se o número de sequência recebido corresponde ao esperado
            if received_msg == 'ACK':
                print('Confirmação recebida:', data.decode())

            seq_num += 1

        except KeyboardInterrupt:
            print("\nConexão encerrada pelo usuário.")
            break

# Fecha a conexão com o servidor
client_socket.close()
print('Conexão fechada')