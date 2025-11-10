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
        self.__livros.append(livro)
        self.salvarLivros()

    def removerLivro(self, livro):
        if livro in self.__livros:
            self.__livros.remove(livro)
            self.salvarLivros()

    def buscarPorId(self, id):
        for livro in self.__livros:
            if livro.getId() == id:
                return livro
        return None

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
                f.write(f"{livro.getId()};{livro.getTitulo()};{livro.getGenero()};"
                        f"{livro.getEditora()};{livro.getAutor()};{livro.getNExemplares()}\n")
