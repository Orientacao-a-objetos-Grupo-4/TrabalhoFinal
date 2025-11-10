import os
from Model.ItensEmprestimo import ItensEmprestimo
from Controller.LivroController import LivroController

class ItensEmprestimoController:
    def __init__(self, arquivo="Data/itensEmprestimo.txt", emprestimoController=None):
        self.__arquivo = arquivo
        self.__itens = []
        self.__livroController = LivroController()
        self.__emprestimoController = emprestimoController  # passado externamente
        self.carregarItens()

    def setEmprestimoController(self, emprestimoController):
        self.__emprestimoController = emprestimoController

    def getItens(self):
        return self.__itens.copy()

    def addItem(self, item):
        if self.buscarPorId(item.getId()) is None:
            self.__itens.append(item)
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
                try:
                    id_str, idLivro_str, idEmprestimo_str = linha.strip().split(";")
                    idLivro = idLivro_str
                    idEmprestimo = idEmprestimo_str

                    livro = self.__livroController.buscarPorId(idLivro)
                    emprestimo = self.__emprestimoController.buscarPorId(idEmprestimo) if self.__emprestimoController else None

                    if livro and emprestimo:
                        item = ItensEmprestimo(id_str, livro, emprestimo)
                        self.__itens.append(item)
                except ValueError:
                    continue

    def salvarItens(self):
        with open(self.__arquivo, "w", encoding="utf-8") as f:
            for item in self.__itens:
                f.write(f"{item.getId()};{item.getLivro().getId()};{item.getEmprestimoLivro().getId()}\n")
