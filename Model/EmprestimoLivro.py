from Untils.Enums import StatusEmprestimo
from datetime import date

class EmprestimoLivro:
    def __init__(self, id, cliente, dataEmprestimo, dataDevolucao, status: StatusEmprestimo = StatusEmprestimo.ATIVO):
        self.__id = id
        self.__cliente = cliente
        self.__dataEmprestimo = dataEmprestimo
        self.__dataDevolucao = dataDevolucao
        self.__status = status
        self.__multa = None
        self.__itens = [] 

    # ---------------- Getters ----------------
    def getId(self):
        return self.__id

    def getCliente(self):
        return self.__cliente

    def getItens(self):
        return self.__itens

    def getDataEmprestimo(self):
        return self.__dataEmprestimo

    def getDataDevolucao(self):
        return self.__dataDevolucao

    def getStatus(self):
        return self.__status

    def getMulta(self):
        return self.__multa

    # ---------------- Setters ----------------
    def setStatus(self, status):
        self.__status = status

    def setDataEmprestimo(self, dataEmprestimo):
        self.__dataEmprestimo = dataEmprestimo

    def setDataDevolucao(self, dataDevolucao):
        self.__dataDevolucao = dataDevolucao

    def setMulta(self, multa):
        self.__multa = multa

    # ---------------- Métodos auxiliares ----------------
    def addItem(self, item_emprestimo):
        self.__itens.append(item_emprestimo)

    def registrarDevolucao(self, dataDevolucao):
        self.setDataDevolucao(dataDevolucao)
        self.setStatus(StatusEmprestimo.DEVOLVIDO)
