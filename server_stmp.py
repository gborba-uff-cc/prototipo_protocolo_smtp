import socket
import sys
import os

from util.processadorProtocolo import processaConexao

# ==============================================================================
if __name__ != '__main__':
    sys.exit(1)
# ==============================================================================


# ==============================================================================
# SECTION - entrada linha de comando
# TODO - receber como argumento de linha de comando o nome de um arquivo e lê-lo.
# NOTE - O arquivo conterá a lista de usuários do serviço de e-mail, um por linha.
# NOTE - verificar se o arquivo com a lista de usuários foi corretamente passado 
# como argumento. Qualquer nesse processo (e.g., arquivo não existe, o formato 
# não é o esperado) deverá gerar uma mensagem de erro e a execução deverá 
# abortar.
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