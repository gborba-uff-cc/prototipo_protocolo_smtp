# NOTE - um cliente basico para interagir com o servidor
# NOTE - este cliente recebe as boas vindas do servidor stmp, entra em um loop 
# de envio de mensagem para o servidor e recebimento de resposta, o loop 
# continua até que o cliente receba a resposta 221 (fim de conexao)
import socket

servidorNome  = 'localhost'
servidorPorta = 49152

# cria o socket para internet protocolo TCP
socketCliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketCliente.connect((servidorNome, servidorPorta))

mensagemBytes = socketCliente.recv(1024)
print('>>> ', mensagemBytes.decode('utf8'))
while True:
    sentenca = input("Digite algo a ser enviado ao servidor:\n<<< ")
    # caso queira enviar uma quebra de linha
    if sentenca == '':
        sentenca = '\n'
    socketCliente.send(sentenca.encode('utf8'))
    mensagemBytes = socketCliente.recv(1024)
    mensagem = mensagemBytes.decode('utf8')
    print('>>> ', mensagem)
    if mensagem.startswith('221'):
        break

socketCliente.close()