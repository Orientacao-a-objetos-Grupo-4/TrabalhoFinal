import os
from Model.Funcionario import Funcionario

class FuncionarioController:
    def __init__(self, arquivo="Data/funcionarios.txt"):
        self.__arquivo = arquivo
        self.__funcionarios = []
        self.carregarFuncionarios()

        if not os.path.exists(self.__arquivo):
            os.makedirs(os.path.dirname(self.__arquivo), exist_ok=True)
            open(self.__arquivo, "w", encoding="utf-8").close()


    def getFuncionarios(self):
        return self.__funcionarios.copy()

    def buscarPorId(self, id):
        for funcionario in self.__funcionarios:
            if funcionario.getId() == id:
                return funcionario
        return None

    def addFuncionario(self, funcionario):
        if self.buscarPorId(funcionario.getId()) is None:
            self.__funcionarios.append(funcionario)
            self.salvarFuncionarios()
            return True
        else:
            print(f"Erro: Funcionário com ID {funcionario.getId()} já existe!")
            return False

    def carregarFuncionarios(self):
        if not os.path.exists(self.__arquivo):
            return

        with open(self.__arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                try:
                    partes = linha.strip().split(";")
                    if len(partes) != 5:
                        print(f"Linha inválida ignorada: {linha.strip()}")
                        continue
                    id_str, nome, login, senha, matricula = partes
                    id = id_str
                    funcionario = Funcionario(id, nome, login, senha, matricula)
                    self.__funcionarios.append(funcionario)
                except ValueError:
                    print(f"Linha inválida no arquivo: {linha.strip()}")
                    continue

    def salvarFuncionarios(self):
        with open(self.__arquivo, "w", encoding="utf-8") as f:
            for func in self.__funcionarios:
                f.write(f"{func.getId()};{func.getNomeUsuario()};{func.getLogin()};{func.getSenha()};{func.getMatricula()}\n")
