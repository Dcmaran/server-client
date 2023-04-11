import socket
import sys
import random
import hashlib
import select
import time

# Configurações do cliente
HOST = '127.0.0.1'  # IP do servidor
PORT = 5000  # Porta do servidor
BUFFER_SIZE = 1024

TIMER =  7
WINDOW_SIZE = 5

seq_num = 0
base = 0
next_seq_num = 0

buffer = {}

def is_parallel(msg):
    return '|' in msg

def send_message(msg):
    msg_id = random.randint(1000, 9999)

    # Calcula a soma de verificação da mensagem
    hash_object = hashlib.sha256(msg.encode())
    checksum = hash_object.hexdigest()

    # Adiciona o número de sequência à mensagem
    msg = f"{msg_id},{seq_num},{msg},{checksum}"

    return msg

def send_window(client_socket):
    global seq_num, buffer
    for i in range(base, min(base + WINDOW_SIZE, seq_num)):
        if i not in buffer:
            continue
        msg = buffer[i]
        client_socket.sendall(msg.encode())
        print(f"Enviando mensagem com número de sequência {i}")

def handle_ack(client_socket):
    global base
    data = client_socket.recv(BUFFER_SIZE)
    ack = data.decode()
    if ack == 'ACK':
        print('Confirmação recebida:', ack)
        base += 1

# Cria um socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta-se ao servidor
client_socket.connect((HOST, PORT))
client_socket.setblocking(0)
print('Conectado ao servidor em', (HOST, PORT))

# Envia mensagens para o servidor
with client_socket:
    while True:
        try:
            print(F"Digite a mensagem (você tem {TIMER} segundos): ", end='', flush=True)
            ready, _, _ = select.select([sys.stdin], [], [], TIMER)

            if ready:
                message = sys.stdin.readline().strip()

                if message == 'sair':
                   print("\nConexão encerrada pelo usuário.")
                   break

                if is_parallel(message):
                    messages = message.split('|')
                    for m in messages:
                        if m == 'sair':
                            print("\nConexão encerrada pelo usuário.")
                            exit(1)

                        while next_seq_num >= base + WINDOW_SIZE:
                            time.sleep(1)
                            handle_ack(client_socket)
                        
                        msg = send_message(m)
                        buffer[next_seq_num] = msg
                        send_window(client_socket)
                        next_seq_num += 1
                        seq_num += 1

                else:
                    while next_seq_num >= base + WINDOW_SIZE:
                        time.sleep(1)
                        handle_ack(client_socket)
                    
                    msg = send_message(message)
                    buffer[next_seq_num] = msg
                    send_window(client_socket)
                    next_seq_num += 1
                    seq_num += 1

            else:
                print(f"\nErro: você não digitou uma mensagem em {TIMER} segundos.")
                continue

            while base < next_seq_num:
                ready, _, _ = select.select([client_socket], [], [], TIMER)
                if ready:
                    handle_ack(client_socket)
                else:
                    print("Reenviando mensagens...")
                    send_window(client_socket)

        except KeyboardInterrupt:
            print("\nConexão encerrada pelo usuário.")
            break

# Fecha a conexão com o servidor

client_socket.close()
print('Conexão fechada')