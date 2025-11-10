import os
from Model.Livro import Livro

class LivroController:
    def __init__(self, arquivo="Data/livros.txt"):
        self.__arquivo = arquivo
        self.__livros = []
        self.carregarLivros()

    def getLivros(self):
        return self.__livros.copy()

    def addLivro(self, livro):
        if self.buscarPorId(livro.getId()) is None:
            self.__livros.append(livro)
            self.salvarLivros()

    def removerLivroPorId(self, id):
        livro = self.buscarPorId(id)
        if livro:
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
                partes = linha.strip().split(";")
                if len(partes) != 6:
                    print(f"Linha inválida ignorada: {linha.strip()}")
                    continue

                id, titulo, genero, editora, autor, nExemplares = partes
                try:
                    livro = Livro(id, titulo, genero, editora, autor, int(nExemplares))
                    self.__livros.append(livro)
                except ValueError:
                    print(f"Erro ao criar livro da linha: {linha.strip()}")
                    continue

    def salvarLivros(self):
        with open(self.__arquivo, "w", encoding="utf-8") as f:
            for livro in self.__livros:
                f.write(f"{livro.getId()};{livro.getTitulo()};{livro.getGenero()};"
                        f"{livro.getEditora()};{livro.getAutor()};{livro.getNExemplares()}\n")
