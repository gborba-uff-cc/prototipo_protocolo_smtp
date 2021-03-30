import socket
import sys
import os
from util.processadorProtocolo import processaConexao

# ==============================================================================
if __name__ != '__main__':
    sys.exit(1)
# ==============================================================================


# ==============================================================================

if len(sys.argv) < 2:
    sys.exit("ERROR: O nome do arquivo não foi passado como argumento!") 

name_arq =  sys.argv[1]
   
try:
    arq = open(name_arq, 'r')
    users = arq.readlines()
    users_list = []
    
    for user in users:
        user = user.rstrip('\n')
        users_list.append(user)
        users_arq = open(user.lower()+".txt", 'w')
        users_arq.close()    
    arq.close()
    
             
except FileNotFoundError as e:
    sys.exit("ERROR: O arquivo não existe!")
           
SERVIDOR_ENDERECO = 'localhost'
# SERVIDOR_PORTA    = 25
SERVIDOR_PORTA    = 49152

# cria socket do servidor
socketServidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# associa o endereco que servidor devera ouvir
socketServidor.bind((SERVIDOR_ENDERECO, SERVIDOR_PORTA))
# permite o servidor aceitar conexões, com no maximo uma conexao na fila
socketServidor.listen(1)
print('Ouvindo na porta {}.\n'.format(SERVIDOR_PORTA))

while True:
    # espera por uma conexao
    print('Esperando nova conexao...')
    socketConexao, enderecoCliente = socketServidor.accept()
    print(
        'Conexao aceita com {}.'.format(enderecoCliente),
        'Iniciando troca de mensagens.',
        'Trocando mensagens...',
        sep='\n'
    )
    try:
        # processa a conexao
        processaConexao(socketConexao)
    except Exception as erro:
        print('Conexao com o cliente foi perdida. {}'.format(erro))
    # fecha a conexao
    socketConexao.close()
    print('Servidor encerrou conexao com cliente.\n')

socketServidor.close()