import socket
import threading

clientes = []

HOST = '0.0.0.0'
PORTA = 9999

def broadcast(mensagem, remetente):
    for cliente in clientes:
        if cliente != remetente:
            try:
                cliente.send(mensagem.encode('utf-8'))
            except Exception as e:
                print("Erro ao enviar:", e)
                if cliente in clientes:
                    clientes.remove(cliente)

def tratar_cliente(conn, addr):
    print(f"[CONEXÃO] {addr} conectado.")

    while True:
        try:
            mensagem = conn.recv(1024).decode('utf-8')

            if not mensagem:
                break

            partes = mensagem.split(':', 1)
            prefixo = partes[0]
            conteudo = partes[1] if len(partes) > 1 else ""

            match prefixo:
                case "MSG":
                    print(f"[{addr}] CHAT: {conteudo}")
                    broadcast(f"[{addr}] {conteudo}", conn)

                case "FILE":
                    print(f"[{addr}] ARQUIVO: {conteudo}")
                    conn.send(f"Servidor pronto para receber {conteudo}".encode('utf-8'))

                case _:
                    print(f"[{addr}] Comando desconhecido")

        except Exception as e:
            print(f"[ERRO] {addr}: {e}")
            break

    print(f"[DESCONEXÃO] {addr} saiu.")

    if conn in clientes:
        clientes.remove(conn)

    conn.close()

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    servidor.bind((HOST, PORTA))
    servidor.listen()

    print(f"[RODANDO] Servidor na porta {PORTA}...")

    while True:
        conn, addr = servidor.accept()

        clientes.append(conn)

        thread = threading.Thread(target=tratar_cliente, args=(conn, addr))
        thread.start()

        print(f"[CLIENTES] {len(clientes)} conectados")

if __name__ == "__main__":
    iniciar_servidor()