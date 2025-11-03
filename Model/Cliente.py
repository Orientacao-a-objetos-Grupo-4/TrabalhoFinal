from enum import Enum
from Model import Usuario


class Cliente(Usuario):
    def __init__(self, nomeUsuario, login, senha,tipo = Enum('ADMINISTRADOR', 'CLIENTE', 'FUNCIONARIO') ):
        super().__init__(nomeUsuario, login, senha,tipo)
        self.__multa = []
        self.__emprestimos = []



    #Multa

    def setMulta(self,multa):
        self.__multa = multa

    def getMulta(self):
        return self.__multa
    
    def addMulta(self,multa):
        self.__multa.append(multa)

    
    def removeMulta(self,multa):
        self.__multa.remove(multa)

    
    #Emprestimo
    def setEmprestimos(self,emprestimos):
        self.__emprestimos = emprestimos

    def getEmprestimos(self):
        return self.__emprestimos
    
    def addEmprestimo(self,emprestimo):
        self.__emprestimos.append(emprestimo)

    
    def removeEmprestimo(self,emprestimo):
        self.__emprestimos.remove(emprestimo)

    #Funcctions

    def buscarLivro(self):
        pass

    
    def solicitarEmprestimo(self):
        pass

    def devolverLivro(self):
        pass
    
    def pagarMulta(self):
        pass   