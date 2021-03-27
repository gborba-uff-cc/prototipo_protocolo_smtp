def enviaTexto(socket, texto, incluiNovaLinha = True):
    '''
    Envia uma string e adiciona uma quebra de linha (\\r\\n) caso incluiNovaLinha seja True.
    incluiNovaLinha por padrão é True.
    '''
    if incluiNovaLinha:
        return socket.send( (texto+'\r\n').encode('UTF8') )
    else:
        return socket.send(texto.encode('UTF8'))

def recebeTexto(socket, removeNovaLinha = False):
    '''
    Recebe uma string.
    '''
    return socket.recv(1024).decode('UTF8')

def removeQuebraLinha(texto):
    '''
    Remove a quebra de linha que existir no fim da string.
    A quebra de linha pode ser tanto '\\r\\n' ou '\\n'.
    '''
    if texto.endswith('\r\n'):
        return texto.rstrip('\r\n')
    elif texto.endswith('\n'):
        return texto.rstrip('\n')

def processaConexao(sConexao):
    NOME_APRESENTACAO = 'smtp.prototipo'
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
    nome_caixa_entrada = ''
    # faz que o comando HELO seja aceito apenas como o primeiro comando
    clienteIdentificado = False
    # mantem a ordem para: MAIL FROM: -> RCPT TO: -> DATA
    ordemComando = 0
    # faz que comando QUIT seja aceito ao enviar no minimo uma mensagem
    mensagemRecebida = False
    # ==========================================================================
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
            # TODO - Testar se dominio do remetente é o mesmo dominio passado no HELO (idCliente)
            ordemComando += 1
            emailRemetente = mensagemTokens[2]
            sConexao.send('250 {} Sender ok'.format(emailRemetente).encode('UTF8'))

        elif mensagem.startswith('RCPT TO:') and quantidadeTokens == 3 and clienteIdentificado and ordemComando == 1:
            # TODO - Testar se dominio do destinatario é o mesmo deste servidor (NOME_APRESENTACAO)
            emailDestinatario = mensagemTokens[2]
            try:
                arq = open(emailDestinatario.split("@")[0] + '.txt', 'r')
                arq.close()
                ordemComando += 1
                sConexao.send('250 {} Recipient ok'.format(emailDestinatario).encode('UTF8'))
            except FileNotFoundError as e:
                ordemComando = 0
                sConexao.send('550 Address unknown'.encode('UTF8'))

        elif mensagem == 'DATA' and quantidadeTokens == 1 and clienteIdentificado and ordemComando == 2:
            ordemComando += 1
            sConexao.send('354 Enter mail, end with ".". on a line by itself'.encode('UTF8'))
            mensagemBytes = sConexao.recv(TAM_BUFFER_RECV)
            mensagem = mensagemBytes.decode('UTF8')
            nome_caixa_entrada = emailDestinatario.split("@")[0]+".txt"
            with open(nome_caixa_entrada, "a") as caixaDeEntrada:
                while mensagem != ".":
                    # TODO - nao acrescentar '\n' caso a mensagem termine com '\n'
                    caixaDeEntrada.write(mensagem + "\n")
                    # REVIEW - tirar linha de debug abaixo
                    print("added {}".format(mensagem + "\n"))
                    mensagemBytes = sConexao.recv(TAM_BUFFER_RECV)
                    mensagem = mensagemBytes.decode('UTF8')
            mensagemRecebida = True
            sConexao.send('250 Message accepted for delivery'.encode('UTF8'))

        elif mensagem == 'QUIT' and quantidadeTokens == 1 and clienteIdentificado and mensagemRecebida and ordemComando == 0:
            terminouConexao = True
            sConexao.send('221 {} closing connection'.format(NOME_APRESENTACAO).encode('UTF8'))

        else:
            sConexao.send('500 Syntax error, command unrecognized'.encode('UTF8'))

        ordemComando %= 3
