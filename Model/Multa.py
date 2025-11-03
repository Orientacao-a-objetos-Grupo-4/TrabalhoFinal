from Untils.Enums import StatusMulta

class Multa:
    def __init__(self, id, valor, status: StatusMulta = StatusMulta.PENDENTE):
        self.__id = id
        self.__valor = valor
        self.__status = status
        self.__emprestimos = []
        self.__cliente = None

    # Getters
    def getValor(self):
        return self.__valor

    def getStatus(self):
        return self.__status

    def getId(self):
        return self.__id

    def getEmprestimos(self):
        return self.__emprestimos

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

    def setCliente(self, cliente):
        self.__cliente = cliente

    # Métodos auxiliares
    def addEmprestimo(self, emprestimo):
        self.__emprestimos.append(emprestimo)

    def removeEmprestimo(self, emprestimo):
        self.__emprestimos.remove(emprestimo)

    def calcularValor(self,dataEmprestimo, dataDevolucao):
        diasAtraso = (dataDevolucao - dataEmprestimo).days
        self.setValor(diasAtraso * 0.1) # Aplicando um acrecimo de 10% por dia de atraso
    
    def registrarPagamento(self):
        self.setStatus(StatusMulta.PAGA)



