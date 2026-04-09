import socket
import threading
import os

# Configuraçoes de Conexao
IP_SERVIDOR = '127.0.0.1' # Use 'localhost' para testar na mesma máquina
PORTA = 9999

def receber_mensagens(sock):
    """Função que rodará em segundo plano para receber dados."""
    while True:
        try:
            dados = sock.recv(1024).decode('utf-8')
            if not dados:
                break
            print(f"\n[MENSAGEM RECEBIDA]: {dados}")
            print("Escolha uma opção (1-3): ", end="") # Re-exibe o prompt
        except:
            print("\n[AVISO] Conexão encerrada pelo servidor.")
            break

def iniciar_cliente():
    # 1. Criando e conectando o socket
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente.connect((IP_SERVIDOR, PORTA))
    except Exception as e:
        return print(f"Não foi possível conectar ao servidor: {e}")

    # 2. Iniciando a thread de escuta
    thread_escuta = threading.Thread(target=receber_mensagens, args=(cliente,), daemon=True)
    thread_escuta.start()

    # 3. Loop do Menu Principal
    while True:
        print("\n" + "="*30)
        print("      SOCKET CHAT & FILE")
        print("="*30)
        print("1. Enviar Mensagem (Chat)")
        print("2. Enviar Arquivo")
        print("3. Sair")
        print("="*30)
        
        opcao = input("Escolha uma opção (1-3): ")

        match opcao:
            case '1':
                msg = input("Digite a mensagem: ")
                cliente.send(f"MSG:{msg}".encode('utf-8'))
            
            case '2':
                caminho = input("Caminho do arquivo: ")
                if os.path.exists(caminho):
                    nome_arq = os.path.basename(caminho)
                    # Por enquanto, enviamos apenas o aviso. 
                    
                    cliente.send(f"FILE:{nome_arq}".encode('utf-8'))
                    print(f"Aviso de arquivo enviado: {nome_arq}")
                else:
                    print("Arquivo não encontrado!")

            case '3':
                cliente.close()
                print("Saindo...")
                break
            
            case _:
                print("Opção inválida!")

if __name__ == "__main__":
    iniciar_cliente()