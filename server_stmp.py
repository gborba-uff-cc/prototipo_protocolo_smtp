import socket
import sys
import os

if __name__ != '__main__':
    sys.exit(1)

# ============================================
def processaConexao(sConexao : socket.socket):
    NOME_APRESENTACAO = 'stmp.prototipo'
    TAM_BUFFER_RECV = 1024
    mensagemBytes = bytes(())
    mensagem = ''
    mensagemTokens = []
    quantidadeTokens = 0
    comandoRecebido = ''
    erro = False
    terminouConexao = False
    idCliente = ''
    emailRemetente = ''
    emailDestinatario = ''
    # faz que o comando HELO aceito apenas como o primeiro comando
    clienteIdentificado = False
    # mantem a ordem para: MAIL FROM: -> RCPT TO: -> DATA
    ordemComando = 0
    # faz que comando QUIT seja aceito ao enviar no minimo uma mensagem
    mensagemRecebida = False

    # 220 <...> ================================================================
    # envia mensagem boas vindas
    sConexao.send('220 {}'.format(NOME_APRESENTACAO).encode('UTF8'))

    while not terminouConexao:
        # recebe mensagem
        mensagemBytes = sConexao.recv(TAM_BUFFER_RECV)
        # decodifica bytes recebidos
        mensagem = mensagemBytes.decode('UTF8')
        # separa em tokens
        mensagemTokens = mensagem.split()
        quantidadeTokens = len(mensagemTokens)

        if mensagem.startswith('HELO') and quantidadeTokens == 2 and not clienteIdentificado:
            clienteIdentificado = True
            idCliente = mensagemTokens[1]
            sConexao.send('250 Hello {}, pleased to meet you'.format(idCliente).encode('UTF8'))

        elif mensagem.startswith('MAIL FROM:') and quantidadeTokens == 3 and clienteIdentificado and ordemComando == 0:
            ordemComando += 1
            emailRemetente = mensagemTokens[2]
            sConexao.send('250 {} Sender ok'.format(emailRemetente).encode('UTF8'))

        elif mensagem.startswith('RCPT TO:') and quantidadeTokens == 3 and clienteIdentificado and ordemComando == 1:
            # SECTION - caso o destinatario nao exista
            # TODO - verificar se o existe a caixa de entrada do destinatario
            # NOTE - caso o destinatário especificado não seja um dos usuários 
            # do sistema, o servidor deverá responder com "550 Address unknown".
            # NOTE - a conexão *não deve ser encerrada nesse caso*.
            # NOTE - pular para o proximo email. (ordemComando = 0)
            # !SECTION
            ordemComando += 1
            emailDestinatario = mensagemTokens[2]
            sConexao.send('250 {} Recipient ok'.format(emailDestinatario).encode('UTF8'))

        elif mensagem == 'DATA' and quantidadeTokens == 1 and clienteIdentificado and ordemComando == 2:
            ordemComando += 1
            sConexao.send('354 Enter mail, end with ".". on a line by itself'.encode('UTF8'))
            # SECTION - receber email
            _ = sConexao.recv(TAM_BUFFER_RECV) # STUB
            # TODO - receber mensagens até receber uma linha com apenas '.' .
            # !SECTION
            mensagemRecebida = True
            sConexao.send('250 Message accepted for delivery'.encode('UTF8'))

        elif mensagem == 'QUIT' and quantidadeTokens == 1 and clienteIdentificado and mensagemRecebida and ordemComando == 0:
            terminouConexao = True
            sConexao.send('221 {} closing connection'.format(NOME_APRESENTACAO).encode('UTF8'))
            # NOTE - Podemos fechar o socket aqui, por enquanto fech no loop do servidor

        else:
            sConexao.send('500 Syntax error, command unrecognized'.encode('UTF8'))

        ordemComando %= 3

# ==============================================================================
# SECTION - entrada linha de comando
# TODO - receber como argumento de linha de comando o nome de um arquivo e lê-lo.
# NOTE - O arquivo conterá a lista de usuários do serviço de e-mail, um por linha.
# NOTE - verificar se o arquivo com a lista de usuários foi corretamente passado como argumento. Qualquer erro na leitura desse processo (e.g., arquivo não existe, o formato não é o esperado) deverá gerar uma mensagem de erro e a execução deverá abortar.
# !SECTION

SERVIDOR_ENDERECO = '127.0.0.1'
SERVIDOR_PORTA = 49152
# SERVIDOR_PORTA = 25

# cria socket do servidor
socketServidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# associa o endereco que servidor devera ouvir
socketServidor.bind((SERVIDOR_ENDERECO, SERVIDOR_PORTA))
# permite o servidor aceitar conexões, com no maximo uma conexao na fila
socketServidor.listen(1)
print('Ouvindo na porta {}.'.format(SERVIDOR_PORTA))

while True:
    # espera por uma conexao
    print('Esperando conexao...')
    socketConexao, enderecoCliente = socketServidor.accept()
    print(
        'Conexao aceita com {}.'.format(enderecoCliente),
        'Iniciando troca de mensagens.',
        'Trocando mensagens',
        sep='\n'
    )
    # processa a conexao
    processaConexao(socketConexao)
    # fecha a conexao
    socketConexao.close()
    print('Servidor encerrou conexao com cliente.\n')

socketServidor.close()