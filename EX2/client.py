import socket

HOST = '127.0.0.1'  # ou IP do servidor
PORT = 10331

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("Conectado ao servidor.")

while True:
    msg = input("Você: ")
    client.send(msg.encode())

    if msg.upper() == "QUIT":
        break

    resposta = client.recv(1024).decode()

    if resposta.upper() == "QUIT":
        print("Servidor encerrou a conexão.")
        break

    print(f"Servidor: {resposta}")

client.close()