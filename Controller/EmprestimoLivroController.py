import os
from datetime import date
from Model.EmprestimoLivro import EmprestimoLivro
from Controller.ItensEmprestimoController import ItensEmprestimoController
from Controller.MultaController import MultaController

class EmprestimoLivroController:
    def __init__(self, arquivo="Data/emprestimos.txt"):
        self.__arquivo = arquivo
        self.__emprestimos = []
        self.__itensController = ItensEmprestimoController()
        self.__multaController = MultaController()
        self.carregarEmprestimos()

    def getEmprestimos(self):
        return self.__emprestimos

    def addEmprestimo(self, emprestimo):
        self.__emprestimos.append(emprestimo)
        self.salvarEmprestimos()

    def removerEmprestimo(self, emprestimo):
        if emprestimo in self.__emprestimos:
            self.__emprestimos.remove(emprestimo)
            self.salvarEmprestimos()

    def buscarPorId(self, id):
        for e in self.__emprestimos:
            if e.getId() == id:
                return e
        return None

    def carregarEmprestimos(self):
        if not os.path.exists(self.__arquivo):
            return
        from Model.Cliente import Cliente
        from Untils.Enums import StatusEmprestimo
        with open(self.__arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                dados = linha.strip().split(";")
                if len(dados) != 5:
                    continue
                id, idCliente, dataEmprestimo, dataDevolucao, status = dados
                cliente = Cliente(idCliente, "", "", "")
                emprestimo = EmprestimoLivro(
                    id,
                    cliente,
                    date.fromisoformat(dataEmprestimo) if dataEmprestimo != "None" else None,
                    date.fromisoformat(dataDevolucao) if dataDevolucao != "None" else None,
                    StatusEmprestimo[status]
                )
                self.__emprestimos.append(emprestimo)

    def salvarEmprestimos(self):
        with open(self.__arquivo, "w", encoding="utf-8") as f:
            for e in self.__emprestimos:
                f.write(f"{e.getId()};{e.getCliente().getId()};{e.getDataEmprestimo()};"
                        f"{e.getDataDevolucao()};{e.getStatus().name}\n")

    # -------- Métodos adicionais integrados --------
    def registrarDevolucao(self, idEmprestimo, dataDevolucao):
        emprestimo = self.buscarPorId(idEmprestimo)
        if not emprestimo:
            print("Empréstimo não encontrado!")
            return

        emprestimo.registrarDevolucao(dataDevolucao)
        self.salvarEmprestimos()

        # Criar multa se houver atraso
        if dataDevolucao > emprestimo.getDataEmprestimo():
            from Model.Multa import Multa
            diasAtraso = (dataDevolucao - emprestimo.getDataEmprestimo()).days
            if diasAtraso > 0:
                valor = diasAtraso * 0.1
                multa = Multa(f"M-{emprestimo.getId()}", valor, emprestimo, emprestimo.getCliente())
                self.__multaController.addMulta(multa)
