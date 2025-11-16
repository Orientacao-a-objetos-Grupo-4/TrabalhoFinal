class Livro:
    def __init__(self, id, titulo, genero, editora, autor, nExemplares):
        self.__id = id
        self.__titulo = titulo
        self.__genero = genero
        self.__editora = editora
        self.__autor = autor
        self.__nExemplares = nExemplares
       

    # Getters
    def getId(self):
        return self.__id

    def getTitulo(self):
        return self.__titulo

    def getGenero(self):
        
        return self.__genero

    def getEditora(self):
        return self.__editora

    def getAutor(self):
        return self.__autor

    def getNExemplares(self):
        return self.__nExemplares

    # Setters
    def setTitulo(self, titulo):
        self.__titulo = titulo

    def setGenero(self, genero):
        self.__genero = genero

    def setEditora(self, editora):
        self.__editora = editora

    def setAutor(self, autor):
        self.__autor = autor

    def setNExemplares(self, nExemplares):
        self.__nExemplares = nExemplares

    # Métodos auxiliares
    def verificarDisponibilidade(self):
        """
        Retorna True se houver exemplares disponíveis.
        """
        return self.getNExemplares() > 0
    
    @staticmethod
    def criarLivro(id, titulo, genero, editora, autor, nExemplares):
        return Livro(id, titulo, genero, editora, autor, nExemplares)

    def retirarExemplar(self):
        """
        Retira um exemplar do estoque.
        """
        if self.verificarDisponibilidade():
            self.setNExemplares(self.getNExemplares() - 1)
            return True
        print(f"O livro '{self.getTitulo()}' está indisponível no momento.")
        return False

    def devolverExemplar(self):
        """
        Devolve um exemplar ao estoque.
        """
        self.setNExemplares(self.getNExemplares() + 1) 

    def to_txt(self):
        """
        Retorna o formato de texto do livro para salvar no arquivo.
        """
        return f"{self.getId()};{self.getTitulo()};{self.getGenero()};{self.getEditora()};{self.getAutor()};{self.getNExemplares()}\n"