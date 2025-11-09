from abc import ABC

from Untils.Enums import TipoUsuario

class Usuario(ABC):
    def __init__(self, id, nomeUsuario, login, senha, tipo: TipoUsuario):
        self.__id = id
        self.__nomeUsuario = nomeUsuario
        self.__login = login
        self.__senha = senha
        self.__cpf = None
        self.__tipo = tipo

    # Getters
    def getNomeUsuario(self):
        return self.__nomeUsuario

    def getLogin(self):
        return self.__login

    def getSenha(self):
        return self.__senha

    def getCpf(self):
        return self.__cpf

    def getTipo(self):
        return self.__tipo
    
    def getId(self):
        return self.__id

    # Setters
    def setNomeUsuario(self, nomeUsuario):
        self.__nomeUsuario = nomeUsuario

    def setLogin(self, login):
        self.__login = login

    def setSenha(self, senha):
        self.__senha = senha

    def setCpf(self, cpf):
        self.__cpf = cpf

    def setTipo(self, tipo):
        if isinstance(tipo, TipoUsuario):
            self.__tipo = tipo
        else:
            print("Tipo de usuário inválido")

