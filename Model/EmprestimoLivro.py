
from Untils.Enums import StatusEmprestimo, StatusMulta


class EmprestimoLivro:
    def __init__(self, id, cliente, livro, dataEmprestimo, dataDevolucao, status: StatusEmprestimo = StatusEmprestimo.ATIVO):
        self.__id = id
        self.__cliente = cliente
        self.__livro = livro
        self.__dataEmprestimo = dataEmprestimo
        self.__dataDevolucao = dataDevolucao
        self.__status = status
        self.__multas = []

    # Getters
    def getId(self):
        return self.__id

    def getCliente(self):
        return self.__cliente

    def getLivro(self):
        return self.__livro

    def getDataEmprestimo(self):
        return self.__dataEmprestimo

    def getDataDevolucao(self):
        return self.__dataDevolucao

    def getStatus(self):
        return self.__status

    def getMultas(self):
        return self.__multas

    # Setters
    def setStatus(self, status):
        self.__status = status

    def setDataEmprestimo(self, dataEmprestimo):
        self.__dataEmprestimo = dataEmprestimo

    def setDataDevolucao(self, dataDevolucao):
        self.__dataDevolucao = dataDevolucao

    # Métodos auxiliares
    def addMulta(self, multa):
        self.__multas.append(multa)

    def removeMulta(self, multa):
        self.__multas.remove(multa)

    def calcularMullta(self):
        pass

    def registrarDevolucao(self, dataDevolucao):
        self.setDataDevolucao(dataDevolucao)
        self.setStatus(StatusEmprestimo.DEVOLVIDO)
     