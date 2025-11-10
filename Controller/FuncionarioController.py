import os
from Model.Funcionario import Funcionario

class FuncionarioController:
    def __init__(self, arquivo="Data/funcionarios.txt"):
        self.__arquivo = arquivo
        self.__funcionarios = []
        self.carregarFuncionarios()

    def getFuncionarios(self):
        return self.__funcionarios

    def buscarPorId(self, id):
        for f in self.__funcionarios:
            if f.getId() == id:
                return f
        return None

    def addFuncionario(self, funcionario):
        if self.buscarPorId(funcionario.getId()) is None:
            self.__funcionarios.append(funcionario)
            self.salvarFuncionarios()
            return True
        else:
            print(f"Erro: Funcionario com ID {funcionario.getId()} já existe!")
            return False

    def carregarFuncionarios(self):
        if not os.path.exists(self.__arquivo):
            return

        with open(self.__arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                try:
                    id_str, nome, login, senha, matricula = linha.strip().split(";")
                    id = int(id_str)  # Garante que ID seja inteiro
                    self.__funcionarios.append(Funcionario(id, nome, login, senha, matricula))
                except ValueError:
                    print(f"Linha inválida no arquivo: {linha.strip()}")

    def salvarFuncionarios(self):
        with open(self.__arquivo, "w", encoding="utf-8") as f:
            for func in self.__funcionarios:
                f.write(f"{func.getId()};{func.getNomeUsuario()};{func.getLogin()};{func.getSenha()};{func.getMatricula()}\n")
