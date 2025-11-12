import os
from Model.Livro import Livro

class LivroController:
    def __init__(self, arquivo="Data/livros.txt"):
        self.__arquivo = arquivo
        self.__livros = []
        self.carregarLivros()

    def getLivros(self):
        return self.__livros

    def addLivro(self, livro):
        if self.buscarPorId(livro.getId()) is None:
            self.__livros.append(livro)
            self.salvarLivros()
        else:
            livro.setNExemplares(livro.getNExemplares() + 1)
            self.salvarLivros()

    def buscarPorId(self, id):
        for livro in self.__livros:
            if livro.getId() == id:
                return livro

    def removerLivroPorId(self, id):
        livro = self.buscarPorId(id)
        if livro:
            self.__livros.remove(livro)
            self.salvarLivros()

    def retirarExemplar(self, id):
        """
        Solicita a retirada de um exemplar de um livro.
        """
        livro = self.buscarPorId(id)
        if livro and livro.retirarExemplar():
            self.salvarLivros()
            return True
        return False

    def devolverExemplar(self, id):
        """
        Solicita a devolução de um exemplar de um livro.
        """
        livro = self.buscarPorId(id)
        if livro:
            livro.devolverExemplar()
            self.salvarLivros()
            return True
        return False

    def carregarLivros(self):
        if not os.path.exists(self.__arquivo):
            return
        with open(self.__arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                id, titulo, genero, editora, autor, nExemplares = linha.strip().split(";")
                livro = Livro(id, titulo, genero, editora, autor, int(nExemplares))
                self.__livros.append(livro)

    def salvarLivros(self):
        with open(self.__arquivo, "w", encoding="utf-8") as f:
            for livro in self.__livros:
                f.write(livro.to_txt())
