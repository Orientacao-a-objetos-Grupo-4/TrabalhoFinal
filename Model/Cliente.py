from Model.Usuario import Usuario
from Untils.Enums import StatusMulta, TipoUsuario

class Cliente(Usuario):
    def __init__(self, id, nomeUsuario, login, senha):
        super().__init__(id, nomeUsuario, login, senha, TipoUsuario.CLIENTE)
        self.__multas = []
        self.__emprestimos = []

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
    def pode_realizar_emprestimo(self):
        """Cliente só pode pegar emprestado se não tiver multas pendentes."""
        return all(m.getStatus() != StatusMulta.PENDENTE for m in self.__multas)

    def realizar_emprestimo(self, emprestimo):
        """Regra de negócio: só empresta se não tiver multas pendentes."""
        if not self.pode_realizar_emprestimo():
            raise Exception(f"{self.getNomeUsuario()} tem multas pendentes e não pode realizar empréstimos.")
        self.__emprestimos.append(emprestimo)

    def devolver_livro(self, emprestimo):
        """Remove o empréstimo da lista."""
        if emprestimo in self.__emprestimos:
            self.__emprestimos.remove(emprestimo)

    def pagar_multa(self, multa_id):
        """Define uma multa como paga."""
        for multa in self.__multas:
            if multa.getId() == multa_id:
                multa.setStatus(StatusMulta.PAGA)
                return True
        raise Exception("Multa não encontrada")

    def registrar_multa(self, multa):
        """Adiciona uma nova multa."""
        self.__multas.append(multa)
