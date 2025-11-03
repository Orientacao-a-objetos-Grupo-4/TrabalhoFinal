from enum import Enum


class Multa:
    def __init__(self, valor,id,status = Enum('PAGA', 'PENDENTE', 'CANCELADA') ):
        self.___id = id
        self.___status = status
        self.___valor = valor
        self.__emprestimos = []
        self.__cliente = None

    #Getters
    def getValor(self):
        return self.___valor
    
    def getStatus(self):
        return self.___status
    
    def getId(self):
        return self.___id
    
    def getEmprestimos(self):
        return self.__emprestimos
    
    def getCliente(self):
        return self.__cliente
    
    #Setters
    def setValor(self,valor):
        self.___valor = valor

    def setStatus(self,status):
        if(status == Enum('PAGA', 'PENDENTE', 'CANCELADA')):
            self.___status = status

        else:
            print('Status inválido')

    def setId(self,id):
        self.___id = id

    def setEmprestimos(self,emprestimos):
        self.__emprestimos = emprestimos

    def setCliente(self,cliente):
        self.__cliente = cliente

    #Untils
    def addEmprestimo(self,emprestimo):
        self.__emprestimos.append(emprestimo)

    def removeEmprestimo(self,emprestimo):
        self.__emprestimos.remove(emprestimo)

    