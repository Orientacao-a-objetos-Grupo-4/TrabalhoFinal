import os
from Model.Multa import Multa
from Untils.Enums import StatusMulta

class MultaController:
    def __init__(self, arquivo="Data/multas.txt", clienteController=None, emprestimoController=None):
        self.__arquivo = arquivo
        self.__multas = []
        self.__clienteController = clienteController
        self.__emprestimoController = emprestimoController
        self.carregarMultas()

    def getMultas(self):
        return self.__multas

    def addMulta(self, multa):
        self.__multas.append(multa)
        self.salvarMultas()

    def removerMulta(self, multa):
        if multa in self.__multas:
            self.__multas.remove(multa)
            self.salvarMultas()

    def removerPorId(self, id):
        multa = self.buscarPorId(id)
        if multa:
            self.__multas.remove(multa)
            self.salvarMultas()

    def buscarPorId(self, id):
        for multa in self.__multas:
            if multa.getId() == id:
                return multa
        return None

    def carregarMultas(self):
        if not os.path.exists(self.__arquivo):
            return
        
        from Model.EmprestimoLivro import EmprestimoLivro
        from Model.Cliente import Cliente

        with open(self.__arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                dados = linha.strip().split(";")
                if len(dados) != 5:
                    continue
                
                id, valor, idEmprestimo, idCliente, status = dados

                try:
                    valor = float(valor)
                    status_enum = StatusMulta[status]
                except (ValueError, KeyError):
                    continue  

                emprestimo = None
                cliente = None

                if self.__emprestimoController:
                    emprestimo = self.__emprestimoController.buscarPorId(idEmprestimo)
                if self.__clienteController:
                    cliente = self.__clienteController.buscarPorId(idCliente)

                if not emprestimo:
                    emprestimo = EmprestimoLivro(idEmprestimo, None, None, None)
                if not cliente:
                    cliente = Cliente(idCliente, "", "", "")

                multa = Multa(id, valor, emprestimo, cliente, status_enum)
                self.__multas.append(multa)

    def salvarMultas(self):
        with open(self.__arquivo, "w", encoding="utf-8") as f:
            for multa in self.__multas:
                f.write(f"{multa.getId()};{multa.getValor()};{multa.getEmprestimo().getId()};"
                        f"{multa.getCliente().getId()};{multa.getStatus().name}\n")
