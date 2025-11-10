import os
from Model.Cliente import Cliente

class ClienteController:
    def __init__(self, arquivo="Data/clientes.txt"):
        self.__arquivo = arquivo
        self.__clientes = []
        self.carregarClientes()

    def getClientes(self):
        return self.__clientes

    def addCliente(self, cliente):
        self.__clientes.append(cliente)
        self.salvarClientes()

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
                id, nome, login, senha = linha.strip().split(";")
                self.__clientes.append(Cliente(id, nome, login, senha))

    def salvarClientes(self):
        with open(self.__arquivo, "w", encoding="utf-8") as f:
            for c in self.__clientes:
                f.write(f"{c.getId()};{c.getNomeUsuario()};{c.getLogin()};{c.getSenha()}\n")
