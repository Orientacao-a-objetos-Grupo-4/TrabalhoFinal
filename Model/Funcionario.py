

from Model.Usuario import Usuario
from Untils.Enums import TipoUsuario


class Funcionario(Usuario):
    def __init__(self, nomeUsuario, login, senha, matricula):
        super().__init__(nomeUsuario, login, senha, TipoUsuario.FUNCIONARIO)
        self.__matricula = matricula

    # Getters e Setters
    def getMatricula(self):
        return self.__matricula

    def setMatricula(self, matricula):
        self.__matricula = matricula

    # Funções (exemplo)
    def cadastrarLivro(self):
        pass

    def cadastrarCliente(self):
        pass

    def cadastrarEmprestimo(self):
        pass

    def registrarDevolucao(self):
        pass
