
# socket cria conexao de rede
# threading permite executar tarefas ao mesmo tempo
# os permite manipular arquivos e caminhos
import socket
import threading
import os

# define ip do servidor para conexao
IP_SERVIDOR = '127.0.0.1'

# define porta usada na comunicacao
PORTA = 9999

# roda em paralelo com o menu principal
def receber_mensagens(sock):
    # loop infinito para escutar dados continuamente
    while True:
        try:
            # recebe ate 1024 bytes do socket e converte para texto
            dados = sock.recv(1024).decode('utf-8')

            # se nao recebeu nada significa que o servidor fechou conexao
            if not dados:
                print("\n[AVISO] Servidor desconectou.")
                break

            # mostra mensagem recebida
            print(f"\n[MENSAGEM]: {dados}")

            # reexibe menu para nao quebrar interacao
            print("Escolha uma opção (1-3): ", end="")

        except Exception:
            print("\n[ERRO] Conexão perdida.")
            break

# funcao principal
def iniciar_cliente():

    # cria socket tcp usando ipv4
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # tenta conectar ao servidor usando ip e porta
    try:
        cliente.connect((IP_SERVIDOR, PORTA))
    except Exception as e:
        print(f"Erro ao conectar: {e}")
        return

    # cria thread para receber mensagens sem travar o menu
    # daemon true encerra thread automaticamente ao fechar programa
    thread = threading.Thread(target=receber_mensagens, args=(cliente,), daemon=True)
    thread.start()

    # loop principal do menu
    while True:

        # imprime interface do menu
        print("\n" + "="*30)
        print("      SOCKET CHAT & FILE")
        print("="*30)
        print("1. Enviar Mensagem")
        print("2. Enviar Arquivo")
        print("3. Sair")
        print("="*30)

        # le opcao 
        opcao = input("Escolha: ")

        try:
            # usa match case para tratar opcoes
            match opcao:

                # opcao 1 envia mensagem 
                case '1':
                    
                    msg = input("Mensagem: ")
                    
                    # encode transforma texto em bytes
                    cliente.send(f"MSG:{msg}".encode('utf-8'))

                # opcao 2 envia arquivo
                case '2':
                 caminho = input("Caminho do arquivo: ")

                 # verifica se arquivo existe no sistema
                 if os.path.exists(caminho):

                    # extrai nome do arquivo
                    nome = os.path.basename(caminho)

                    # pega tamanho em bytes do arquivo
                    tamanho = os.path.getsize(caminho)
        
                    # envia cabecalho com tipo nome e tamanho
                    cliente.send(f"FILE:{nome}:{tamanho}".encode('utf-8'))
        
                    # abre arquivo em modo binario leitura
                    with open(caminho, 'rb') as f:

                     # le arquivo em blocos de 1024 bytes
                     while True:
                        bytes_lidos = f.read(1024)

                        # se nao houver mais dados encerra envio
                        if not bytes_lidos:
                            break

                        # envia bloco de bytes para o servidor
                        cliente.send(bytes_lidos)

                        # informa sucesso no envio
                        print("Arquivo enviado com sucesso 🚀")

                 # caso arquivo nao exista
                 else:
                    print("Arquivo não encontrado.")

                # opcao 3 encerra programa
                case '3':
                    print("Saindo...")

                    # fecha conexao com servidor
                    cliente.close()
                    break

                
                case _:
                    print("Opção inválida.")

        # trata erro ao enviar dados
        except Exception as e:
            print(f"[ERRO] Falha ao enviar: {e}")
            print("Servidor pode ter caído.")
            break


# executa funcao principal 
if __name__ == "__main__":
    iniciar_cliente()