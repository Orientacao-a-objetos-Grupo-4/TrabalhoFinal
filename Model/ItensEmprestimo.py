
#precisamos de quantidade pq pode ser que o cliente pegue mais de um exemplar do mesmo livro?
#podemos criar o ID utilizando o ID do emprestimo + ID do livro

class ItensEmprestimo:
    def __init__(self, id,livro,  emprestimoLivro):
        self.__id = id
        self.__livro = livro
        self.__emprestimoLivro = emprestimoLivro

    # Getters
    def getLivro(self):
        return self.__livro
    
    def getId(self):
        return self.__id


    def getEmprestimoLivro(self):
        return self.__emprestimoLivro

    # Setters
    def setLivro(self, livro):
        self.__livro = livro

    def setId(self, id):
        self.__id = id


    def setEmprestimoLivro(self, emprestimoLivro):
        self.setEmprestimoLivro = emprestimoLivro

    def registrarEmprestimo(self):
        """
        Reduz o número de exemplares disponíveis do livro emprestado.
        """
        self.getLivro().retirarExemplar()

    def registrarDevolucao(self):
        """
        Aumenta o número de exemplares disponíveis do livro devolvido.
        """
        self.getLivro().devolverExemplar()

    def to_txt(self):
        """
        Retorna o formato de texto para salvar no arquivo.
        """
        return f"{self.getId()};{self.getLivro().getId()};{self.getEmprestimoLivro().getId()}\n"
