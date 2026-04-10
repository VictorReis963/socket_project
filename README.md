# 🔌 Socket Project — Redes de Computadores

**Universidade Presbiteriana Mackenzie — Faculdade de Computação e Informática**  
Disciplina: Redes de Computadores | Prof. Dr. Bruno da Silva Rodrigues

**Integrantes:**
- Gabriel Lazareti Cardoso — RA: 10417353
- Victor Hugo Fiuza Garcia — RA: 10331903
- Victor Reis da Silva — RA: 10420297

---

## 📁 Estrutura do Repositório

```
socket_project/
├── EX2/
│   ├── client.py       # Cliente TCP com chat e encerramento por QUIT
│   └── server.py       # Servidor TCP que aceita uma conexão por vez
├── Ex3/
│   ├── client.py       # Cliente com menu: chat e envio de arquivos
│   ├── server.py       # Servidor multi-cliente com threads e broadcast
│   └── teste.txt       # Arquivo de exemplo para testar o envio
└── README.md
```

---

## 🎬 Vídeos de Demonstração

| Atividade | Link |
|-----------|------|
| Vídeo 1 — Questões 1 e 2 (Chat TCP/UDP) | [https://youtu.be/wVdZc2c3g1E](https://youtu.be/wVdZc2c3g1E) |
| Vídeo 2 — Questão 3 (Aplicação com Threads + Arquivos) | [https://youtu.be/Lr8zIiQOM_Q](https://youtu.be/Lr8zIiQOM_Q) |

---

## ✅ Questão 2 — Chat TCP com QUIT (`EX2/`)

Chat bidirecional entre cliente e servidor via **TCP**. A conexão é encerrada quando qualquer uma das partes envia o comando `QUIT`.

- **Protocolo:** TCP (`SOCK_STREAM`)
- **Porta:** `10331` (primeiros 5 dígitos do TIA)
- **Host padrão:** `127.0.0.1`

### Como executar

> ⚠️ O servidor deve ser iniciado **antes** do cliente. Em TCP, o cliente tenta estabelecer conexão imediatamente — sem servidor ativo, a conexão é recusada.

**Terminal 1 — Servidor:**
```bash
cd EX2
python server.py
```

**Terminal 2 — Cliente:**
```bash
cd EX2
python client.py
```

Para encerrar, qualquer lado digita:
```
QUIT
```

---

## 🚀 Questão 3 — Chat Multi-Cliente + Envio de Arquivos (`Ex3/`)

Aplicação TCP com suporte a **múltiplos clientes simultâneos via threads**. Cada cliente conectado pode:

1. **Enviar mensagens de chat** — transmitidas via broadcast para todos os outros clientes conectados
2. **Enviar arquivos** — o servidor recebe e salva localmente; os demais clientes são notificados

- **Protocolo:** TCP (`SOCK_STREAM`)
- **Porta:** `9999`
- **Host padrão:** `127.0.0.1`
- **Threads:** cada cliente é tratado em uma thread independente (`threading.Thread`)

### Protocolo de mensagens

| Prefixo | Formato | Descrição |
|---------|---------|-----------|
| `MSG`   | `MSG:<texto>` | Mensagem de chat — distribuída via broadcast |
| `FILE`  | `FILE:<nome>:<tamanho_bytes>` + bytes do arquivo | Envio de arquivo em blocos de 1024 bytes |

### Como executar

**Terminal 1 — Servidor:**
```bash
cd Ex3
python server.py
```

**Terminais 2, 3, ... — Clientes (um por terminal):**
```bash
cd Ex3
python client.py
```

No menu interativo do cliente, escolha:
```
==============================
      SOCKET CHAT & FILE
==============================
1. Enviar Mensagem
2. Enviar Arquivo
3. Sair
==============================
```

Para testar o envio de arquivo, use o `teste.txt` incluso ou qualquer outro arquivo informando o **caminho completo**.

> Arquivos recebidos pelo servidor são salvos no diretório de execução com o prefixo `recebido_`.

---

## 🧰 Requisitos

- Python 3.10+ (necessário para `match/case`)
- Bibliotecas utilizadas: `socket`, `threading`, `os` — todas nativas do Python

Nenhuma instalação adicional é necessária.

---

## 📚 Referências

- KUROSE, J. F.; ROSS, K. W. *Redes de Computadores e a Internet — Uma Nova Abordagem*. Pearson.
- [Internet Engineering Task Force — IETF](https://www.ietf.org)
