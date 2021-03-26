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
            # SECTION - receber email
            _ = sConexao.recv(TAM_BUFFER_RECV) # STUB
            # NOTE - abrir a caixa de entrada do destinatario (arquivo).
            # TODO - receber mensagens até receber uma linha com apenas '.'.
            # NOTE - acrescentar'\n' na mensagem antes de apender ao arquivo.
            # !SECTION
            mensagemRecebida = True
            sConexao.send('250 Message accepted for delivery'.encode('UTF8'))

        elif mensagem == 'QUIT' and quantidadeTokens == 1 and clienteIdentificado and mensagemRecebida and ordemComando == 0:
            terminouConexao = True
            sConexao.send('221 {} closing connection'.format(NOME_APRESENTACAO).encode('UTF8'))

        else:
            sConexao.send('500 Syntax error, command unrecognized'.encode('UTF8'))

        ordemComando %= 3
