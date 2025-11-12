import os
from Model.Cliente import Cliente

class ClienteController:
    def __init__(self, arquivo="Data/clientes.txt"):
        self.__arquivo = arquivo
        self.__clientes = []
        self.__garantir_arquivo()
        self.carregarClientes()

    def __garantir_arquivo(self):
        os.makedirs(os.path.dirname(self.__arquivo), exist_ok=True)
        if not os.path.exists(self.__arquivo):
            open(self.__arquivo, "w", encoding="utf-8").close()

    # --- Getters ---
    def getClientes(self):
        return self.__clientes.copy()

    def buscarPorId(self, id):
        for c in self.__clientes:
            if c.getId() == id:
                return c
        return None

    # --- CRUD ---
    def criarCliente(self, id, nome, login, senha):
        if self.buscarPorId(id):
            raise Exception("Cliente com esse ID já existe.")
        cliente = Cliente(id, nome, login, senha)
        self.__clientes.append(cliente)
        self.salvarClientes()
        return cliente

    def addCliente(self, cliente):
        if self.buscarPorId(cliente.getId()):
            raise Exception("Cliente com esse ID já existe.")
        self.__clientes.append(cliente)
        self.salvarClientes()

    # --- Regras de negócio ---
    def registrarMulta(self, cliente_id, multa):
        cliente = self.buscarPorId(cliente_id)
        if not cliente:
            raise Exception("Cliente não encontrado.")
        cliente.registrarMulta(multa)
        self.salvarClientes()

    def realizarEmprestimo(self, cliente_id, emprestimo):
        cliente = self.buscarPorId(cliente_id)
        if not cliente:
            raise Exception("Cliente não encontrado.")
        cliente.realizarEmprestimo(emprestimo)
        self.salvarClientes()

    def pagarMulta(self, cliente_id, multa_id):
        cliente = self.buscarPorId(cliente_id)
        if not cliente:
            raise Exception("Cliente não encontrado.")
        cliente.pagarMulta(multa_id)
        self.salvarClientes()

    def salvarClientes(self):
        os.makedirs(os.path.dirname(self.__arquivo), exist_ok=True)
        with open(self.__arquivo, "w", encoding="utf-8") as f:
            for cliente in self.__clientes:
                multas_ids = ",".join(str(m.getId()) for m in cliente.getMultas())
                emprestimos_ids = ",".join(str(e.getId()) for e in cliente.getEmprestimos())
                f.write(
                    f"{cliente.getId()};{cliente.getNomeUsuario()};{cliente.getLogin()};"
                    f"{cliente.getSenha()};{multas_ids};{emprestimos_ids}\n"
                )

    def carregarClientes(self):
        if not os.path.exists(self.__arquivo):
            return
        with open(self.__arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                partes = linha.strip().split(";")
                if len(partes) < 4:
                    continue
                id, nome, login, senha = partes[:4]
                cliente = Cliente(int(id), nome, login, senha)
                self.__clientes.append(cliente)
