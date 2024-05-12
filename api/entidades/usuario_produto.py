class Usuario_produto():
    def __init__(self, id_usuario, id_produto, quantidade_produto):
        self.__nome = id_usuario
        self.__id_produto = id_produto
        self.__quantidade_produto = quantidade_produto


    @property
    def id_usuario(self):
        return self.__id_usuario

    @id_usuario.setter
    def id_usuario(self, id_usuario):
        self.__id_usuario = id_usuario

    @property
    def id_produto(self):
        return self.__id_produto

    @id_produto.setter
    def id_produto(self, id_produto):
        self.__id_produto = id_produto

    @property
    def quantidade_produto(self):
        return self.__quantidade_produto

    @quantidade_produto.setter
    def quantidade_produto(self, quantidade_produto):
        self.__quantidade_produto = quantidade_produto
