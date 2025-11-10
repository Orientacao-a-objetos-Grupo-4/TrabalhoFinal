import os
from Model.ItensEmprestimo import ItensEmprestimo
from Controller.LivroController import LivroController
from Controller.EmprestimoLivroController import EmprestimoController

class ItensEmprestimoController:
    def __init__(self, arquivo="Data/itensEmprestimo.txt"):
        self.__arquivo = arquivo
        self.__itens = []
        self.__livroController = LivroController()
        self.__emprestimoController = EmprestimoController()
        self.carregarItens()

    def getItens(self):
        return self.__itens

    def addItem(self, item):
        if self.buscarPorId(item.getId()) is None:
            self.__itens.append(item)
            self.salvarItens()

    def removerItemPorId(self, id):
        item = self.buscarPorId(id)
        if item:
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
        
        with open(self.__arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                id, idLivro, idEmprestimo = linha.strip().split(";")
                
                # Busca os objetos reais via controllers
                livro = self.__livroController.buscarPorId(idLivro)
                emprestimo = self.__emprestimoController.buscarPorId(idEmprestimo)
                
                if livro and emprestimo:  # só adiciona se ambos existirem
                    item = ItensEmprestimo(id, livro, 1, emprestimo)
                    self.__itens.append(item)

    def salvarItens(self):
        with open(self.__arquivo, "w", encoding="utf-8") as f:
            for item in self.__itens:
                f.write(f"{item.getId()};{item.getLivro().getId()};{item.getEmprestimoLivro().getId()}\n")
