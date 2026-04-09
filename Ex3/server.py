import socket
import threading

clientes=[]

# configurações do servidor
HOST = '0.0.0.0'  # escuta em todas as redes disponiveis
PORTA = 9999
def broadcast(mensagem, remetente):
    print("Broadcastando para", len(clientes), "clientes")
    for cliente in clientes:
        print("Enviando para:", cliente)
        try:
            cliente.send(mensagem.encode('utf-8'))
        except Exception as e:
            print("Erro:", e)

def tratar_cliente(conn, addr):
    print(f"[CONEXÃO] {addr} conectado.")
    conectado = True
    
    while conectado:
        try:
            # recebe o cabeçalho da mensagem
            mensagem = conn.recv(1024).decode('utf-8')
            if not mensagem:
                break

            # processando com match/case
            prefixo = mensagem.split(':', 1)[0]
            conteudo = mensagem.split(':', 1)[1] if ':' in mensagem else ""

            match prefixo:
                case "MSG":
                    print(f"[{addr}] CHAT: {conteudo}")

                    broadcast(f"[{addr}] {conteudo}", conn)
                
                case "FILE":
                    print(f"[{addr}] SOLICITAÇÃO DE ARQUIVO: {conteudo}")
                    # Aqui entrara a logica de recebimento de bytes
                    conn.send(f"Servidor pronto para receber {conteudo}".encode('utf-8'))
                
                case _:
                    print(f"[{addr}] Enviou um comando desconhecido.")
        
        except Exception as e:
            print(f"[ERRO] Erro com o cliente {addr}: {e}")
            break

    print(f"[DESCONEXÃO] {addr} saiu.")
    conn.close()

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORTA))
    servidor.listen()
    conn, addr = servidor.accept()
    clientes.append(conn)
    print(f"[RODANDO] Servidor aguardando conexões em {PORTA}...")

    while True:
        conn, addr = servidor.accept()
        # Cria uma thread para cada novo cliente
        thread = threading.Thread(target=tratar_cliente, args=(conn, addr))
        thread.start()
        print(f"[CONEXÕES ATIVAS] {threading.active_count() - 1}")

if __name__ == "__main__":
    iniciar_servidor()