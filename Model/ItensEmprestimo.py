class ItensEMprestimo:
    def __init__(self, livro, quantidade, emprestimoLivro):
        self.__livro = livro
        self.__quantidade = quantidade
        self.__emprestimoLivro = emprestimoLivro


    #GETTERS
    def getLivro(self):
        return self.__livro
    
    def getQuantidade(self):
        return self.__quantidade
    
    def getEmprestimoLivro(self):
        return self.__emprestimoLivro
    

    #SETTERS
    def setLivro(self,livro):
        self.__livro = livro

    def setQuantidade(self,quantidade):
        self.__quantidade = quantidade

    def setEmprestimoLivro(self,emprestimoLivro):
        self.__emprestimoLivro = emprestimoLivro

        