import os
from Model.Multa import Multa
from Untils.Enums import StatusMulta

class MultaController:
    def __init__(self, arquivo="Data/multas.txt", clienteController=None, emprestimoController=None):
        self.__arquivo = arquivo
        self.__multas = []
        self.__clienteController = clienteController
        self.__emprestimoController = emprestimoController

        if not os.path.exists(os.path.dirname(self.__arquivo)):
            os.makedirs(os.path.dirname(self.__arquivo), exist_ok=True)
        if not os.path.exists(self.__arquivo):
            open(self.__arquivo, "w", encoding="utf-8").close()

        self.carregarMultas()

        if not os.path.exists(self.__arquivo):
            os.makedirs(os.path.dirname(self.__arquivo), exist_ok=True)
            open(self.__arquivo, "w", encoding="utf-8").close()

    def getMultas(self):
        return self.__multas

    def criarMulta(self, valor, emprestimo, cliente):
        multa = Multa.criarMulta(emprestimo, cliente, valor)
        if multa:
            print("Multa criada com sucesso!")
            self.addMulta(multa)
            return multa
        print("Erro ao criar a multa.")
        return None

    def buscarPorId(self, id):
        for multa in self.__multas:
            if multa.getId() == id:
                return multa
        return None

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

    def calcularMulta(self, id):
        multa = self.buscarPorId(id)
        if multa:
            multa.calcularValor()
            self.salvarMultas()
            return multa.getValor()
        print("Multa não encontrada.")
        return 0.0

    def pagarMulta(self, id):
        multa = self.buscarPorId(id)
        if multa:
            multa.registrarPagamento()
            self.salvarMultas()
            print(f"Multa {id} paga com sucesso!")
        else:
            print("Multa não encontrada.")

    def carregarMultas(self):
        if not os.path.exists(self.__arquivo):
            return


        from Model.EmprestimoLivro import EmprestimoLivro
        from Model.Usuario import Usuario

        with open(self.__arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                dados = linha.strip().split(";")
                if len(dados) != 5:
                    continue

                id, valor, idEmprestimo, idCliente, status = dados

                try:
                    valor = float(valor_str)
                    status_enum = StatusMulta[status_str]
                    idEmprestimo = idEmprestimo_str
                    idCliente = idCliente_str
                except (ValueError, KeyError):
                    continue
                