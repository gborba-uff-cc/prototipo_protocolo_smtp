# NOTE - um cliente basico para interagir com o servidor
# NOTE - este cliente recebe as boas vindas do servidor smtp, entra em um loop 
# de envio de mensagem para o servidor e recebimento de resposta, o loop 
# continua até que o cliente receba a resposta 221 (fim de conexao)
import socket
from util.processadorProtocolo import (enviaTexto,recebeTexto,removeQuebraLinha)

SERVIDOR_ENDERECO = 'localhost'
# SERVIDOR_PORTA    = 25
SERVIDOR_PORTA    = 49152

# cria o socket para internet protocolo TCP
socketCliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketCliente.connect((SERVIDOR_ENDERECO, SERVIDOR_PORTA))

mensagem = recebeTexto(socketCliente)
print('>>> ', mensagem, end='')
while True:
    sentenca = input("Digite algo a ser enviado ao servidor:\n<<< ")
    # caso queira enviar uma quebra de linha
    enviaTexto(socketCliente, sentenca)
    mensagem = recebeTexto(socketCliente)
    print('>>> ', mensagem, end='')
    if mensagem.startswith('354'):
        while True:
            sentenca = input("Digite algo a ser enviado ao servidor:\n<<< ")
            if removeQuebraLinha(sentenca) == '.':
                enviaTexto(socketCliente, sentenca)
                mensagem = recebeTexto(socketCliente)
                print('>>> ', mensagem, end='')
                break
            enviaTexto(socketCliente, sentenca)
    elif mensagem.startswith('221'):
        break

socketCliente.close()