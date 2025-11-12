import os
from Model.ItensEmprestimo import ItensEmprestimo
from Controller.LivroController import LivroController


class ItensEmprestimoController:
    def __init__(self, arquivo="Data/itensEmprestimo.txt", emprestimoController=None, livroController=None):
        self.__arquivo = arquivo
        self.__itens = []
        self.__livroController = livroController
        self.__emprestimoController = emprestimoController
        self.carregarItens()

    def getItens(self):
        return self.__itens

    def buscarPorId(self, id):
        for item in self.__itens:
            if item.getId() == id:
                return item
        return None
    
    def setLivroController(self, livroController):
        self.__livroController = livroController

    def setEmprestimoController(self, emprestimoController):
        self.__emprestimoController = emprestimoController

    def addItem(self, item: ItensEmprestimo):
        if self.buscarPorId(item.getId()) is None:
            # chama a lógica de negócio dentro do model
            item.registrarEmprestimo()
            self.__itens.append(item)
            self.salvarItens()
            return True
        else:
            print(f"Erro: Item de empréstimo com ID {item.getId()} já existe!")
            return False

    def removerItem(self, id):
        """
        Remove um item e devolve o exemplar do livro.
        """
        item = self.buscarPorId(id)
        if item:
            item.registrarDevolucao()
            self.__itens.remove(item)
            self.salvarItens()

    def carregarItens(self):
        if not os.path.exists(self.__arquivo):
            return

        with open(self.__arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                try:
                    id_str, idLivro_str, idEmprestimo_str = linha.strip().split(";")
                    livro = self.__livroController.buscarPorId(idLivro_str)
                    emprestimo = self.__emprestimoController.buscarPorId(idEmprestimo_str) if self.__emprestimoController else None

                    if livro and emprestimo:
                        item = ItensEmprestimo(id_str, livro, emprestimo)
                        self.__itens.append(item)
                except ValueError:
                    continue

    def salvarItens(self):
        with open(self.__arquivo, "w", encoding="utf-8") as f:
            for item in self.__itens:
                f.write(item.to_txt())
