# usando __identificador  para privado
# usando  _identificador  para protegido
# usando   identificador  para publico

class MaquinaEstados():
    def __init__(self, estadoInicial, estadoFinal):
        self.__maquinaValidada = False
        self.__estadoInicial = estadoInicial
        self.__estadoAtual = estadoInicial
        self.__estadoFinal = estadoFinal
        self.__estados = {}
        self.__transicoes = {}

    def adicionaEstado(self, identificadorEstado, estadoMaquina):
        """
        Define um par, identificador e estado a ser identificado, dentro da maquina.
        """
        self.__estados[identificadorEstado] = estadoMaquina

    def adicionaTrasicao(self, estadoOrigem, sinal, estadoDestino):
        """
        Define uma transição entre dois estados juntamente com o sinal/gatilho 
        que ativa essa transição, aceita apenas um sinal por transição.
        """
        chave = self.__chaveTransicoes(estadoOrigem, sinal)
        self.__transicoes[chave] = estadoDestino


class EstadosMaquina():
    def __init__(self,
        funcaoAoEntrar      = lambda *args, **kwargs : 0,
        funcaoAoExecutar    = lambda *args, **kwargs : 0,
        funcaoAoSair        = lambda *args, **kwargs : 0
    ):
        """
        OBS.: A maneira de passar parametros para as callbacks dos estados é 
        por parametros e parametros nomeados,
        ex. de parametro nomeado: funcao(nome=valor)
        e dentro da cada função pegar o par nome=valor usando, 
        ex.: nome = kwargs.get('nome', valor_caso_nome_nao_exista) 
        onde a variavel nome conterá o valor passado como parametro nomeado ou 
        o valor para caso o parametro não tenha sido passado.
        """
        self.__funcaoAoEntrar    = funcaoAoEntrar
        self.__funcaoAoExecutar  = funcaoAoExecutar
        self.__funcaoAoSair      = funcaoAoSair

    """
    Funcao que deve ser executada ao 
    """
    @property
    def funcaoAoEntrar(self):
        return self.__funcaoAoEntrar

    @property
    def funcaoAoExecutar(self):
        return self.__funcaoAoExecutar

    @property
    def funcaoAoSair(self):
        return self.__funcaoAoSair
