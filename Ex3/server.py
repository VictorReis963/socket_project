import socket
import threading

# Configurações do Servidor
HOST = '0.0.0.0'  # Escuta em todas as redes disponíveis
PORTA = 9999

def tratar_cliente(conn, addr):
    print(f"[CONEXÃO] {addr} conectado.")
    conectado = True
    
    while conectado:
        try:
            # Recebe o cabeçalho da mensagem
            mensagem = conn.recv(1024).decode('utf-8')
            if not mensagem:
                break

            # Processando com Match/Case (Python 3.10+)
            prefixo = mensagem.split(':', 1)[0]
            conteudo = mensagem.split(':', 1)[1] if ':' in mensagem else ""

            match prefixo:
                case "MSG":
                    print(f"[{addr}] CHAT: {conteudo}")
                    # Opcional: Enviar confirmação de volta
                    conn.send("Mensagem recebida pelo servidor!".encode('utf-8'))
                
                case "FILE":
                    print(f"[{addr}] SOLICITAÇÃO DE ARQUIVO: {conteudo}")
                    # Aqui entrará a lógica de recebimento de bytes no futuro
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
    servidor.bind((HOST, PORTA))
    servidor.listen()
    print(f"[RODANDO] Servidor aguardando conexões em {PORTA}...")

    while True:
        conn, addr = servidor.accept()
        # Cria uma thread para cada novo cliente
        thread = threading.Thread(target=tratar_cliente, args=(conn, addr))
        thread.start()
        print(f"[CONEXÕES ATIVAS] {threading.active_count() - 1}")

if __name__ == "__main__":
    iniciar_servidor()