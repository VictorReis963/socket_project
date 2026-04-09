import socket
import threading
import os

IP_SERVIDOR = '127.0.0.1'
PORTA = 9999

def receber_mensagens(sock):
    while True:
        try:
            dados = sock.recv(1024).decode('utf-8')

            if not dados:
                print("\n[AVISO] Servidor desconectou.")
                break

            print(f"\n[MENSAGEM]: {dados}")
            print("Escolha uma opção (1-3): ", end="")

        except Exception:
            print("\n[ERRO] Conexão perdida.")
            break

def iniciar_cliente():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        cliente.connect((IP_SERVIDOR, PORTA))
    except Exception as e:
        print(f"Erro ao conectar: {e}")
        return

    thread = threading.Thread(target=receber_mensagens, args=(cliente,), daemon=True)
    thread.start()

    while True:
        print("\n" + "="*30)
        print("      SOCKET CHAT & FILE")
        print("="*30)
        print("1. Enviar Mensagem")
        print("2. Enviar Arquivo")
        print("3. Sair")
        print("="*30)

        opcao = input("Escolha: ")

        try:
            match opcao:
                case '1':
                    msg = input("Mensagem: ")
                    cliente.send(f"MSG:{msg}".encode('utf-8'))

                case '2':
                    caminho = input("Caminho do arquivo: ")

                    if os.path.exists(caminho):
                        nome = os.path.basename(caminho)
                        cliente.send(f"FILE:{nome}".encode('utf-8'))
                        print("Arquivo enviado (nome).")
                    else:
                        print("Arquivo não encontrado.")

                case '3':
                    print("Saindo...")
                    cliente.close()
                    break

                case _:
                    print("Opção inválida.")

        except Exception as e:
            print(f"[ERRO] Falha ao enviar: {e}")
            print("Servidor pode ter caído.")
            break

if __name__ == "__main__":
    iniciar_cliente()