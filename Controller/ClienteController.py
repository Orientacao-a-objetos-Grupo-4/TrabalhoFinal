import os
from Model.Cliente import Cliente

import os
from Model.Cliente import Cliente

class ClienteController:
    def __init__(self, arquivo="Data/clientes.txt"):
        self.__arquivo = arquivo
        self.__clientes = []
        self.carregarClientes()

        if not os.path.exists(self.__arquivo):
            os.makedirs(os.path.dirname(self.__arquivo), exist_ok=True)
            open(self.__arquivo, "w", encoding="utf-8").close()

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
                    partes = linha.strip().split(";")
                    if len(partes) < 4:
                        continue  # Linha inválida
                    id = partes[0]
                    nome = partes[1]
                    login = partes[2]
                    senha = partes[3]

                    cliente = Cliente(id, nome, login, senha)

                    if len(partes) > 4 and partes[4]:
                        cliente._Cliente__multas = [mid for mid in partes[4].split(",")]

                    if len(partes) > 5 and partes[5]:
                        cliente._Cliente__emprestimos = [eid for eid in partes[5].split(",")]

                    self.__clientes.append(cliente)
                except ValueError:
                    print(f"Linha inválida ignorada: {linha}")
                    continue

    def salvarClientes(self):
        with open(self.__arquivo, "w", encoding="utf-8") as f:
            for c in self.__clientes:
                # Salvar apenas IDs
                multas_str = ",".join(
                    str(m.getId()) if hasattr(m, "getId") else str(m)
                    for m in c.getMultas()
                )
                emprestimos_str = ",".join(
                    str(e.getId()) if hasattr(e, "getId") else str(e)
                    for e in c.getEmprestimos()
                )
                f.write(f"{c.getId()};{c.getNomeUsuario()};{c.getLogin()};{c.getSenha()};{multas_str};{emprestimos_str}\n")

    def carregarMultasReais(self, multa_controller):
        for cliente in self.__clientes:
            novas_multas = []
            for mid in cliente.getMultas():
                multa_obj = multa_controller.buscarPorId(mid)
                if multa_obj:
                    novas_multas.append(multa_obj)
            cliente._Cliente__multas = novas_multas

    def carregarEmprestimosReais(self, emprestimo_controller):
        for cliente in self.__clientes:
            novos_emprestimos = []
            for eid in cliente.getEmprestimos():
                emprestimo_obj = emprestimo_controller.buscarPorId(eid)
                if emprestimo_obj:
                    novos_emprestimos.append(emprestimo_obj)
            cliente._Cliente__emprestimos = novos_emprestimos


