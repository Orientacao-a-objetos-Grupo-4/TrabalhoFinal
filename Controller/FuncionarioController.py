import os
from Model.Funcionario import Funcionario

class FuncionarioController:
    def __init__(self, arquivo="Data/funcionarios.txt"):
        self.__arquivo = arquivo
        self.__funcionarios = []
        self.carregarFuncionarios()

    def getFuncionarios(self):
        return self.__funcionarios

    def addFuncionario(self, funcionario):
        self.__funcionarios.append(funcionario)
        self.salvarFuncionarios()

    def buscarPorId(self, id):
        for f in self.__funcionarios:
            if f.getId() == id:
                return f
        return None

    def carregarFuncionarios(self):
        if not os.path.exists(self.__arquivo):
            return
        with open(self.__arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                id, nome, login, senha, matricula = linha.strip().split(";")
                self.__funcionarios.append(Funcionario(id, nome, login, senha, matricula))

    def salvarFuncionarios(self):
        with open(self.__arquivo, "w", encoding="utf-8") as f:
            for func in self.__funcionarios:
                f.write(f"{func.getId()};{func.getNomeUsuario()};{func.getLogin()};{func.getSenha()};{func.getMatricula()}\n")
