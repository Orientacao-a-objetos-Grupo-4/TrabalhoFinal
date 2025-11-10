import os
from Model.ItensEmprestimo import ItensEmprestimo

class ItensEmprestimoController:
    def __init__(self, arquivo="Data/itensEmprestimo.txt"):
        self.__arquivo = arquivo
        self.__itens = []
        self.carregarItens()

    def getItens(self):
        return self.__itens

    def addItem(self, item):
        self.__itens.append(item)
        self.salvarItens()

    def removerItem(self, item):
        if item in self.__itens:
            self.__itens.remove(item)
            self.salvarItens()

    def buscarPorId(self, id):
        for item in self.__itens:
            if item.getId() == id:
                return item
        return None

    def carregarItens(self):
        if not os.path.exists(self.__arquivo):
            return
        from Model.Livro import Livro
        from Model.EmprestimoLivro import EmprestimoLivro
        with open(self.__arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                id, idLivro, idEmprestimo = linha.strip().split(";")
                livro = Livro(idLivro, "", "", "", "", 0)
                emprestimo = EmprestimoLivro(idEmprestimo, None, None, None)
                item = ItensEmprestimo(id, livro, 1, emprestimo)
                self.__itens.append(item)

    def salvarItens(self):
        with open(self.__arquivo, "w", encoding="utf-8") as f:
            for item in self.__itens:
                f.write(f"{item.getId()};{item.getLivro().getId()};{item.getEmprestimoLivro().getId()}\n")
