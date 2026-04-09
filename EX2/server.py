import socket

HOST = '0.0.0.0'
PORT = 10331

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"Servidor ouvindo na porta {PORT}...")

conn, addr = server.accept()
print(f"Conectado com {addr}")

while True:
    msg = conn.recv(1024).decode()
    
    if msg.upper() == "QUIT":
        print("Cliente encerrou a conexão.")
        break

    print(f"Cliente: {msg}")

    resposta = input("Você: ")
    conn.send(resposta.encode())

    if resposta.upper() == "QUIT":
        break

conn.close()
server.close()