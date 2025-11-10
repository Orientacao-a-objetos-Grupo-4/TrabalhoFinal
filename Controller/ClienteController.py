import os
from Model.Cliente import Cliente

class ClienteController:
    def __init__(self, arquivo="Data/clientes.txt"):
        self.__arquivo = arquivo
        self.__clientes = []
        self.carregarClientes()

    def getClientes(self):
        return self.__clientes.copy()

    def addCliente(self, cliente):
        if self.buscarPorId(cliente.getId()) is None:
            self.__clientes.append(cliente)
            self.salvarClientes()
        else:
            print(f"Cliente com ID {cliente.getId()} já existe!")

    def buscarPorId(self, id):
        for c in self.__clientes:
            if c.getId() == id:
                return c
        return None

    def carregarClientes(self):
        if not os.path.exists(self.__arquivo):
            return
        with open(self.__arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                try:
                    id_str, nome, login, senha = linha.strip().split(";")
                    id = int(id_str)  # converter ID para inteiro, se necessário
                    self.__clientes.append(Cliente(id, nome, login, senha))
                except ValueError:
                    # Ignora linhas mal formatadas
                    continue

    def salvarClientes(self):
        with open(self.__arquivo, "w", encoding="utf-8") as f:
            for c in self.__clientes:
                f.write(f"{c.getId()};{c.getNomeUsuario()};{c.getLogin()};{c.getSenha()}\n")
