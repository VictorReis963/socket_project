
# socket cria comunicacao de rede
# threading permite varios clientes ao mesmo tempo
import socket
import threading

# lista global que guarda todos os clientes conectados
clientes = []

# define host escutando todas as redes
HOST = '0.0.0.0'

# define porta do servidor
PORTA = 9999

# funcao que envia mensagem para todos os clientes
def broadcast(mensagem, remetente):

    # percorre lista de clientes conectados
    for cliente in clientes:

        # evita enviar para quem mandou
        if cliente != remetente:
            try:
                # envia mensagem convertida para bytes
                cliente.send(mensagem.encode('utf-8'))

            except Exception as e:
                print("Erro ao enviar:", e)

                # remove cliente com problema da lista
                if cliente in clientes:
                    clientes.remove(cliente)

# funcao que trata comunicacao com um cliente especifico
def tratar_cliente(conn, addr):

    # mostra quando cliente conectados existem
    print(f"[CONEXÃO] {addr} conectado.")

    # loop continuo para receber dados
    while True:
        try:
            # recebe dados do cliente
            mensagem = conn.recv(1024).decode('utf-8')

            # se nao receber nada 
            if not mensagem:
                break

            # separa tipo da mensagem e conteudo
            partes = mensagem.split(':', 1)
            prefixo = partes[0]
            conteudo = partes[1] if len(partes) > 1 else ""

            # verifica tipo da mensagem
            match prefixo:

                # caso seja mensagem de chat
                case "MSG":

                    # mostra no servidor
                    print(f"[{addr}] CHAT: {conteudo}")

                    # envia para outros clientes
                    broadcast(f"[{addr}] {conteudo}", conn)

                # caso seja envio de arquivo
                case "FILE":
                    try:
                        # separa nome e tamanho do arquivo
                        nome, tamanho = conteudo.split(':')

                        tamanho = int(tamanho)

                        # mostra inicio do recebimento
                        print(f"[{addr}] Recebendo arquivo: {nome} ({tamanho} bytes)")

                        # abre arquivo para escrita em binario
                        with open(f"recebido_{nome}", 'wb') as f:

                            # contador de bytes recebidos
                            bytes_recebidos = 0

                            # loop ate receber todo o arquivo
                            while bytes_recebidos < tamanho:

                                 # recebe bloco de dados
                                 dados = conn.recv(1024)

                                 # escreve no arquivo
                                 f.write(dados)

                                 # soma quantidade recebida
                                 bytes_recebidos += len(dados)

                        print(f"[{addr}] Arquivo recebido com sucesso!")

                        # avisa outros clientes
                        broadcast(f"{addr} enviou o arquivo {nome}", conn)

                    # erro durante recebimento
                    except Exception as e:
                        print("Erro ao receber arquivo:", e)

                case _:
                    print(f"[{addr}] Comando desconhecido")

        # erro geral de conexao
        except Exception as e:
            print(f"[ERRO] {addr}: {e}")
            break

    # cliente saiu da conexao
    print(f"[DESCONEXÃO] {addr} saiu.")

    # remove cliente da lista se ainda estiver nela
    if conn in clientes:
        clientes.remove(conn)

    # fecha conexao com cliente
    conn.close()

# funcao principal do servidor
def iniciar_servidor():

    # cria socket tcp ipv4
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # permite reutilizar porta rapidamente
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # associa socket ao ip e porta
    servidor.bind((HOST, PORTA))

    # coloca servidor em modo de escuta
    servidor.listen()

    print(f"[RODANDO] Servidor na porta {PORTA}...")

    # loop infinito aguardando conexoes
    while True:

        # aceita nova conexao
        conn, addr = servidor.accept()

        # adiciona cliente na lista global
        clientes.append(conn)

        # cria thread para tratar cliente separado
        thread = threading.Thread(target=tratar_cliente, args=(conn, addr))
        thread.start()

        # mostra quantidade de clientes conectados
        print(f"[CLIENTES] {len(clientes)} conectados")


if __name__ == "__main__":
    iniciar_servidor()