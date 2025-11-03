from Model.Usuario import Usuario
from Untils.Enums import TipoUsuario

class Cliente(Usuario):
    def __init__(self, nomeUsuario, login, senha):
        super().__init__(nomeUsuario, login, senha, TipoUsuario.CLIENTE)
        self.__multas = []
        self.__emprestimos = []

    # Multas
    def getMultas(self):
        return self.__multas

    def addMulta(self, multa):
        self.__multas.append(multa)

    def removeMulta(self, multa):
        self.__multas.remove(multa)

    # Empréstimos
    def getEmprestimos(self):
        return self.__emprestimos

    def addEmprestimo(self, emprestimo):
        self.__emprestimos.append(emprestimo)

    def removeEmprestimo(self, emprestimo):
        self.__emprestimos.remove(emprestimo)

    # Funções
    def buscarLivro(self):
        pass

    def solicitarEmprestimo(self):
        pass

    def devolverLivro(self):
        pass

    def pagarMulta(self):
        pass
