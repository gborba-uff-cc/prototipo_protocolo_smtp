class MaquinaEstados():
    def __init__(self, estadoInicial, estadoFinal):
        self.__maquinaValidada = False
        self.__estadoInicial = estadoInicial
        self.__estadoAtual = estadoInicial
        self.__estadoFinal = estadoFinal
        self.__estados = {}
        self.__transicoes = {}


class EstadosMaquina():
    def __init__(self,
        funcaoAoEntrar      = lambda *args, **kwargs : 0,
        funcaoAoExecutar    = lambda *args, **kwargs : 0,
        funcaoAoSair        = lambda *args, **kwargs : 0
    ):
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
