import os
import uuid
from Model.Livro import Livro

class LivroController:
    def __init__(self, arquivo="Data/livros.txt"):
        self.__arquivo = arquivo
        self.__livros = []
        self.carregarLivros()

        if not os.path.exists(self.__arquivo):
            os.makedirs(os.path.dirname(self.__arquivo), exist_ok=True)
            open(self.__arquivo, "w", encoding="utf-8").close()

    def getLivros(self):
        return self.__livros


    def criarLivro(self, titulo, genero, editora, autor, n_exemplares):
        
        livro = Livro.criarLivro(uuid.uuid4(), titulo, genero, editora, autor, n_exemplares)
        self.addLivro(livro)
        return livro

    def addLivro(self, livro):
        if self.buscarPorId(livro.getId()) is None:
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
            
    def buscarPorTitulo(self, titulo):
        for livro in self.__livros:
            if livro.getTitulo() == titulo:
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
                id = uuid.UUID(id)
                livro = Livro(id, titulo, genero, editora, autor, int(nExemplares))
                self.__livros.append(livro)

    def salvarLivros(self):
        with open(self.__arquivo, "w", encoding="utf-8") as f:
            for livro in self.__livros:
                f.write(livro.to_txt())
