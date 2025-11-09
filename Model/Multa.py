from Untils.Enums import StatusMulta
from Model.EmprestimoLivro import EmprestimoLivro

#retirei a lista de emprestimos, pq a multa está vinculada a um emprestimo especifico

class Multa:
    def __init__(self, id, valor, emprestimo, cliente, status: StatusMulta = StatusMulta.PENDENTE):
        self.__id = id
        self.__valor = valor
        self.__status = status
        self.__emprestimo = emprestimo
        self.__cliente = cliente

    # Getters
    def getValor(self):
        return self.__valor

    def getStatus(self):
        return self.__status

    def getId(self):
        return self.__id

    def getEmprestimo(self):
        return self.__emprestimo

    def getCliente(self):
        return self.__cliente

    # Setters
    def setValor(self, valor):
        self.__valor = valor

    def setStatus(self, status):
        if isinstance(status, StatusMulta):
            self.__status = status
        else:
            print("Status inválido")
    
    def setEmrpestimo(self, emprestimo):
        self.__emprestimo = emprestimo

    def setCliente(self, cliente):
        self.__cliente = cliente

    # Métodos auxiliares

    def calcularValor(self,dataEmprestimo, dataDevolucao):
        diasAtraso = (dataDevolucao - dataEmprestimo).days
        self.setValor(diasAtraso * 0.1) # Aplicando um acrecimo de 10% por dia de atraso
    
    def registrarPagamento(self):
        self.setStatus(StatusMulta.PAGA)



