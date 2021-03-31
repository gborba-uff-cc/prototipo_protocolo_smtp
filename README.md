# prototipo_protocolo_smtp

Implementação de um protótipo simplificado de servidor de e-mail (SMTP)
utilizando sockets.

---

## Execução

* Acesse a pasta raiz do projeto e execute o script server_smtp.py com um
interpretador python3.

* Ao executar o script python do servidor, é preciso passar o nome de um arquivo
que contem uma lista de nomes de usuário (caixas de entrada). Exemplo:

    ```bash
    python3 server_smtp.py users.txt
    ```

* O arquivo com a lista de nomes de usuário deve conter um nome de usuário por
linha, e cada nome será utilizado para criar uma caixa de entrada para esse
usuário. Exemplo:

    ```txt
    johndoe
    jhaneroe
    babydoe
    ```

* A troca de mensagem com este servidor pode ser realizado via telnet ou
executando script do cliente fornecido. Este servidor e o cliente fornecido
funcionam por padrão na porta 49152 (essa porta é para evitar conflitos com
processos que já estejam em execução no Sistema Operacional.)

    ```bash
    telnet 127.0.0.1 49152
    ```

    OU,

    ```bash
    pyhton3 cliente.py
    ```

## Observações

* Caso necessário, a mudança de número da porta do servidor e do cliente podem
ser modificadas mudando o valor da variável `SERVIDOR_PORTA` no script
`server_smtp.py` e no script `cliente.py`.

* A cada conexao com um cliente, este servidor SMTP responderá a comandos
seguindo uma ordem específica. Sendo essa ordem: helo, mail from, rcpt to, data
e quit.

* Este servidor SMTP cria as caixas de entrada utilizando os nomes fornecidos no
arquivo passado como argumento; observe que todos os nomes serão lidos com os
caracteres minúsculos. Exemplo: `JohnDoe` será interpretado como `johndoe`.

* Este servidor SMTP não distingue comandos com caracteres maúisculos de
minúsculos, portanto: `MAIL FROM: FOO@EXAMPLE`, `MAIL FROM: foo@example` e
`mail from: foo@example` são reconhecidos como o mesmo comando.

* O email passado no comando mail from será associado a uma caixa de entrada.

* A diferenciação das caixas de entrada será feita usando somente os caracteres
que precedem o '@' (ou todos os caracteres caso não exista '@'). Com isso emails
enviados para `johndoe`, `johnDoe@example` e `johndoe@example.example` serão
direcionadas para a mesma caixa de entrada `johndoe.txt`.

* O comando quit só pode ser enviado após o comando data e depois de pelo menos
uma mensagem ter sido enviada.

* Para esse servidor receber várias mensagens em uma única conexao, o cliente
precisa seguir a ordem dos comandos até antes do quit e, onde anteriormente
seria enviado o quit, o cliente deve enviar o comando mail from e seguir a ordem
dos comandos.

* Caso o cliente envie algum comando que não exista, ou envie um comando que não
esteja da maneira especificada no caso de uso, o servidor responderá com o erro
"500 Syntax error, command unrecognized".
Por exemplo, cliente envia: `helo`, o servidor neste caso respondera com o erro
e esperará o envio do comando válido neste caso por exemplo `helo teste`.
Cliente envia o comando `mail from: johndoe` logo após outro mail from, neste
caso o servidor responderá com a mensagem de erro e esperará receber o comando
rcpt to, por exemplo: `rcpt to: babydoe`.

## Caso de uso

* ### Nome: Recebe email

* ### Cenário típico

    1. > **servidor** envia boas vindas ao cliente

    2. > **cliente** envia comando `helo dominio`, onde dominio pode ser
    qualquer string

    3. > **servidor** confirma que o dominio foi aceito

    4. > **cliente** envia comando `mail from: email`, onde email pode ser
    qualquer string

    5. > **servidor** confirma que o email do remetente foi aceito

    6. > **cliente** envia comando `rcpt to: email`, onde email pode ser
    qualquer nome_usuario que esteja contido no arquivo passado como argumento ao servidor.

    7. > **servidor** confirma que o email do destinatario foi aceito

    8. > **cliente** envia comando `data`

    9. > **servidor** avisa que estará recebendo o corpo da mensagem enquanto
    não receber "."

    10. > **cliente** envia as linhas do corpo do email e mais uma linha com "."

    11. > **servidor** confirma recebimento do corpo do email

    12. > **cliente** envia comando `quit`

    13. > **servidor** confirma o intuito de termino da comunicação

* ### Cenarios alternativos

  * 6. **cliente** envia comando `rcpt to: email`, e o email não corresponde a
    uma caixa de entrada nesse servidor.
        1. > **servidor** envia erro "550 Address unknown"
        2. > retorna ao passo 4 do fluxo do principal

  * 12. **cliente** envia comando `mail from: email@dominio1`
        1. > retorna ao passo 5 do fluxo principal

### ***Integrantes do grupo:***

* Jorge Stief

* Ronald Maymone

* Vitor Rocha

* Gabriel Borba

* Matheus Costa Maia Perrut
