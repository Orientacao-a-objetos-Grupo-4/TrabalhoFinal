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
        return self.__nExemplares > 0

    def retirarExemplar(self):
        if self.verificarDisponibilidade():
            self.__nExemplares -= 1
        else:
            print("Nenhum exemplar disponível.")

    def devolverExemplar(self):
        self.__nExemplares += 1
