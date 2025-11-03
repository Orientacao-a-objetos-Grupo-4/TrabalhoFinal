from enum import Enum
from Model import Usuario


class FUncionario(Usuario):
    def __init__(self, nomeUsuario, login, senha,matricula,tipo = Enum('ADMINISTRADOR', 'CLIENTE', 'FUNCIONARIO') ):
        self.__matricula = matricula
        super().__init__(nomeUsuario, login, senha,tipo)

    #Getters
    def getMatricula(self):
        return self.__matricula
    
    #Setters
    def setMatricula(self,matricula):
        self.__matricula = matricula


    #Functions
    def cadastrarLivro(self):
        pass

    def cadastrarCliente(self):
        pass

    def cadastrarEmprestimo(self):
        pass

    def registrarDevolucao(self):
        pass

