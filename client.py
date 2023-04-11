import socket
import sys
import random
import hashlib
import threading
import tkinter as tk

# Configurações do cliente
HOST = '127.0.0.1'  # IP do servidor
PORT = 5000  # Porta do servidor
BUFFER_SIZE = 1024
TIMER = 7000  # 7 segundos

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

def receive_ack(client_socket):
    global seq_num
    while True:
        data = client_socket.recv(BUFFER_SIZE)
        received_msg = data.decode()

        if received_msg == 'ACK':
            seq_num += 1
            reset_timer()

def send_message_with_ack(event=None):
    global seq_num
    message = entry_var.get()
    entry_var.set('')

    if message.strip() == 'sair':
        add_to_textbox("\nConexão encerrada pelo usuário.\n")
        client_socket.close()
        window.quit()
        return

    if isParallel(message):
        messages = message.split('|')

        for i in messages:
            if i.strip() == 'sair':
                add_to_textbox("\nConexão encerrada pelo usuário.\n")
                client_socket.close()
                window.quit()
                return

            mensagem = send_message(i)
            client_socket.sendall(mensagem.encode())
            window.after(TIMER, resend_message, mensagem)
    else:
        mensagem = send_message(message)
        client_socket.sendall(mensagem.encode())
        window.after(TIMER, resend_message, mensagem)

def resend_message(mensagem):
    global seq_num
    if seq_num == int(mensagem.split(',')[1]):
        add_to_textbox(f'Reenviando a mensagem: {mensagem}\n')
        client_socket.sendall(mensagem.encode())
        window.after(TIMER, resend_message, mensagem)

def add_to_textbox(text):
    textbox.configure(state='normal')
    textbox.insert(tk.END, text)
    textbox.configure(state='disabled')
    textbox.see(tk.END)

def reset_timer():
    timer_var.set(TIMER)

def update_timer():
    value = timer_var.get()
    if value > 0:
        value -= 100
        timer_var.set(value)
        window.after(100, update_timer)
    else:
        reset_timer()

# Cria um socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta-se ao servidor
client_socket.connect((HOST, PORT))

# Inicializa a interface gráfica
window = tk.Tk()
window.title("Cliente")

entry_var = tk.StringVar()

textbox = tk.Text(window, wrap=tk.WORD, height=15, width=50, state='disabled')
textbox.grid(row=0, column=0, padx=10, pady=10)

entry = tk.Entry(window, textvariable=entry_var, width=50)
entry.grid(row=1, column=0, padx=10, pady=(0, 10))
entry.bind('<Return>', send_message_with_ack)

send_button = tk.Button(window, text="Enviar", command=send_message_with_ack)
send_button.grid(row=1, column=1, padx=(0, 10), pady=(0, 10))

timer_var = tk.IntVar(value=TIMER)
timer_label = tk.Label(window, textvariable=timer_var)
timer_label.grid(row=2, column=0, padx=10, pady=(0, 10))

#Inicializa a thread para receber ACKs do servidor
ack_thread = threading.Thread(target=receive_ack, args=(client_socket,))
ack_thread.daemon = True
ack_thread.start()

#Inicializa o temporizador
update_timer()

#Inicia o loop principal da interface gráfica
window.mainloop()

# Fecha a conexão com o servidor
client_socket.close()