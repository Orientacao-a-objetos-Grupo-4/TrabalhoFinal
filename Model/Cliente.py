from Model.Usuario import Usuario
from Untils.Enums import StatusMulta, TipoUsuario

class Cliente(Usuario):
    def __init__(self, id: int, nome_usuario: str, login: str, senha: str):
        super().__init__(id, nome_usuario, login, senha, TipoUsuario.CLIENTE)
        self.__multas = []
        self.__emprestimos = []

    # --- Getters ---
    def getMultas(self):
        return self.__multas.copy()

    def getEmprestimos(self):
        return self.__emprestimos.copy()

    def getMultasPorStatus(self, status):
        return [m for m in self.__multas if m.getStatus() == status]

    # --- Multas ---
    def addMulta(self, multa):
        self.__multas.append(multa)

    def removeMulta(self, multa):
        if multa in self.__multas:
            self.__multas.remove(multa)

    def pagarMulta(self, multa_id):
        multa = next((m for m in self.__multas if m.getId() == multa_id), None)
        if not multa:
            raise Exception("Multa não encontrada.")
        multa.setStatus(StatusMulta.PAGA)

    def registrarMulta(self, multa):
        self.__multas.append(multa)

    # --- Empréstimos ---
    def addEmprestimo(self, emprestimo):
        self.__emprestimos.append(emprestimo)

    def removeEmprestimo(self, emprestimo):
        if emprestimo in self.__emprestimos:
            self.__emprestimos.remove(emprestimo)

    def podeRealizarEmprestimo(self):
        """Cliente só pode pegar emprestado se não tiver multas pendentes."""
        return all(m.getStatus() != StatusMulta.PENDENTE for m in self.__multas)

    def realizarEmprestimo(self, emprestimo):
        """Regra de negócio: só empresta se não tiver multas pendentes."""
        if not self.podeRealizarEmprestimo():
            raise Exception(f"{self.getNomeUsuario()} tem multas pendentes e não pode realizar empréstimos.")
        self.addEmprestimo(emprestimo)

    def devolverLivro(self, emprestimo):
        """Remove o empréstimo da lista."""
        self.removeEmprestimo(emprestimo)
