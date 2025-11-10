
#precisamos de quantidade pq pode ser que o cliente pegue mais de um exemplar do mesmo livro?
#podemos criar o ID utilizando o ID do emprestimo + ID do livro

class ItensEmprestimo:
    def __init__(self, livro, quantidade, emprestimoLivro):
        self.__id = id
        self.__livro = livro
        self.__quantidade = quantidade
        self.__emprestimoLivro = emprestimoLivro

    # Getters
    def getLivro(self):
        return self.__livro
    
    def getId(self):
        return self.__id

    def getQuantidade(self):
        return self.__quantidade

    def getEmprestimoLivro(self):
        return self.__emprestimoLivro

    # Setters
    def setLivro(self, livro):
        self.__livro = livro

    def setId(self, id):
        self.__id = id

    def setQuantidade(self, quantidade):
        self.__quantidade = quantidade

    def setEmprestimoLivro(self, emprestimoLivro):
        self.__emprestimoLivro = emprestimoLivro
