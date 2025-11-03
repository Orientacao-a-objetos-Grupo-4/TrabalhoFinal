from Model.Usuario import Usuario
from Untils.Enums import StatusMulta, TipoUsuario

class Cliente(Usuario):
    def __init__(self, nomeUsuario, login, senha,id):
        self.__id = id
        super().__init__(nomeUsuario, login, senha, TipoUsuario.CLIENTE)
        self.__multas = []
        self.__emprestimos = []


    def getId(self):
        return self.__id
    
    def setId(self, id):
        self.__id = id

    # Multas
    def getMultas(self):
        return self.__multas
    
    def getMultasPendentes(self):
        return [multa for multa in self.__multas if multa.getStatus() == StatusMulta.PENDENTE]
    
    def getMultasPagas(self):
        return [multa for multa in self.__multas if multa.getStatus() == StatusMulta.PAGA]
    
    def getMultasCanceladas(self):
        return [multa for multa in self.__multas if multa.getStatus() == StatusMulta.CANCELADA]
    
    def getMulta(self, id):
        return [multa for multa in self.__multas if multa.getId() == id][0]
    

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
