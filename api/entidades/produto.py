class Produto():
    def __init__(self, nome, descricao, data_publicacao, categoria, quantidade, imagem):
        self.__nome = nome
        self.__descricao = descricao
        self.__data_publicacao = data_publicacao
        self.__categoria = categoria
        self.__quantidade = quantidade
        self.__imagem = imagem

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def descricao(self):
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao):
        self.__descricao = descricao

    @property
    def data_publicacao(self):
        return self.__data_publicacao

    @data_publicacao.setter
    def data_publicacao(self, data_publicacao):
        self.__data_publicacao = data_publicacao

    @property
    def categoria(self):
        return self.__categoria

    @categoria.setter
    def categoria(self, categoria):
        self.__categoria = categoria

    @property
    def quantidade(self):
        return self.__quantidade

    @quantidade.setter
    def quantidade(self, quantidade):
        self.__quantidade = quantidade

    @property
    def imagem(self):
        return self.__imagem

    @imagem.setter
    def imagem(self, imagem):
        self.__imagem = imagem

