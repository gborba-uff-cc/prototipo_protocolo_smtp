import socket
import sys
import os

if __name__ != '__main__':
    sys.exit(1)

# ============================================
def processaConexao(sConexao : socket.socket):
    mensagemBytes = bytes(())
    mensagemTokens = []
    comandoRecebido = ''
    erro = False
    terminouConexao = False
    idCliente = ''
    emailRemetente = ''
    emailDestinatario = ''

    # 220 <...> ================================================================
    # envia mensagem
    sConexao.send('220 stmp.prototype'.encode('UTF8'))

    # HELO <...> ===============================================================
    # recebe mensagem
    mensagemBytes = sConexao.recv(1024)
    # decodifica bytes recebidos
    mensagemTokens = mensagemBytes.decode('UTF8').split()
    # pega comando
    comandoRecebido = mensagemTokens[0]
    # verifica inconsistencia e se o comando passado foi HELO <...>
    erro = len(mensagemTokens) != 2 or comandoRecebido != 'HELO'
    while erro:
        # envia mensagem de erro
        sConexao.send('500 Syntax error, command unrecognized'.encode('UTF8'))
        # recebe mensagem
        mensagemBytes = sConexao.recv(1024)
        # decodifica bytes recebidos
        mensagemTokens = mensagemBytes.decode('UTF8').split()
        # pega comando
        comandoRecebido = mensagemTokens[0]
        # verifica inconsistencia e se o comando passado foi HELO <...>
        erro = len(mensagemTokens) != 2 or comandoRecebido != 'HELO'
    # adquire informacao
    idCliente = mensagemTokens[1]

    # 250 <...> {idCliente}<...> ===============================================
    sConexao.send('250 Hello {}, pleased to meet you'.format(idCliente).encode('UTF8'))

    # TODO daqui para baixo executar em loop até receber quit
    # MAIL FROM: <...> =====================================================
    mensagemBytes = sConexao.recv(1024)
    mensagemTokens = mensagemBytes.decode('UTF8').split()
    try:
        comandoRecebido = '{} {}'.format(mensagemTokens[0], mensagemTokens[1])
    except Exception:
        comandoRecebido = ''
    erro = len(mensagemTokens) != 3 or comandoRecebido != 'MAIL FROM:'
    while erro:
        sConexao.send('500 Syntax error, command unrecognized'.encode('UTF8'))
        mensagemBytes = sConexao.recv(1024)
        mensagemTokens = mensagemBytes.decode('UTF8').split()
        try:
            comandoRecebido = '{} {}'.format(mensagemTokens[0], mensagemTokens[1])
        except Exception:
            comandoRecebido = ''
        erro = len(mensagemTokens) != 3 or comandoRecebido != 'MAIL FROM:'
    emailRemetente = mensagemTokens[2]

    # 250 {emailRemetente} <...> ===========================================
    sConexao.send('250 {} Sender ok'.format(emailRemetente).encode('UTF8'))

    # RCPT TO: <...> =======================================================
    mensagemBytes = sConexao.recv(1024)
    mensagemTokens = mensagemBytes.decode('UTF8').split()
    try:
        comandoRecebido = '{} {}'.format(mensagemTokens[0], mensagemTokens[1])
    except Exception:
        comandoRecebido = ''
    erro = len(mensagemTokens) != 3 or comandoRecebido != 'RCPT TO:'
    while erro:
        sConexao.send('500 Syntax error, command unrecognized'.encode('UTF8'))
        mensagemBytes = sConexao.recv(1024)
        mensagemTokens = mensagemBytes.decode('UTF8').split()
        try:
            comandoRecebido = '{} {}'.format(mensagemTokens[0], mensagemTokens[1])
        except Exception:
            comandoRecebido = ''
        erro = len(mensagemTokens) != 3 or comandoRecebido != 'RCPT TO:'
    emailDestinatario = mensagemTokens[2]

    # 250 {emailDestinatario} <...> ========================================
    sConexao.send('250 {} Recipient ok'.format(emailDestinatario).encode('UTF8'))

    # DATA =================================================================
    mensagemBytes = sConexao.recv(1024)
    mensagemTokens = mensagemBytes.decode('UTF8').split()
    comandoRecebido = mensagemTokens[0]
    erro = len(mensagemTokens) != 1 or comandoRecebido != 'DATA'
    while erro:
        sConexao.send('500 Syntax error, command unrecognized'.encode('UTF8'))
        mensagemBytes = sConexao.recv(1024)
        mensagemTokens = mensagemBytes.decode('UTF8').split()
        comandoRecebido = mensagemTokens[0]
        erro = len(mensagemTokens) != 1 or comandoRecebido != 'DATA'

    # 354 <...> ============================================
    sConexao.send('354 Enter mail, end with ".". on a line by itself'.encode('UTF8'))

    # <...> ================================================================
    # TODO rebebimento do conteudo até até receber uma linha com apenas '.'

    # 250 <...> ============================================
    sConexao.send('250 Message accepted for delivery'.encode('UTF8'))



SERVIDOR_ENDERECO = '127.0.0.1'
SERVIDOR_PORTA = 49152
# SERVIDOR_PORTA = 25

# cria socket do servidor
socketServidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# associa o endereco que servidor devera ouvir
socketServidor.bind((SERVIDOR_ENDERECO, SERVIDOR_PORTA))
# permite o servidor aceitar conexões, com no maximo uma conexao na fila
socketServidor.listen(1)

while True:
    # espera por uma conexao
    socketConexao, enderecoCliente = socketServidor.accept()
    # processa a conexao
    processaConexao(socketConexao)
    # fecha a conexao
    socketConexao.close()

socketServidor.close()