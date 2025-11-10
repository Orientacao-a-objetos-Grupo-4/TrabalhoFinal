import os
from datetime import date
import uuid
from Model.EmprestimoLivro import EmprestimoLivro
from Model.Multa import Multa
from Untils.Enums import StatusEmprestimo, StatusMulta

class EmprestimoLivroController:
    def __init__(self, arquivo="Data/emprestimos.txt"):
        self.__arquivo = arquivo
        self.__emprestimos = []
        self.__itensController = None
        self.__clienteController = None
        self.__multaController = None
        self.carregarEmprestimos()

        if not os.path.exists(self.__arquivo):
            os.makedirs(os.path.dirname(self.__arquivo), exist_ok=True)
            open(self.__arquivo, "w", encoding="utf-8").close()

    # ---------------- Setters para controllers cruzados ----------------
    def setItensController(self, itensController):
        self.__itensController = itensController

    def setClienteController(self, clienteController):
        self.__clienteController = clienteController

    def setMultaController(self, multaController):
        self.__multaController = multaController

    # ---------------- Getters ----------------
    def getEmprestimos(self):
        return self.__emprestimos.copy()

    # ---------------- Funções CRUD ----------------
    def addEmprestimo(self, emprestimo):
        self.__emprestimos.append(emprestimo)
        self.salvarEmprestimos()

    def buscarPorId(self, id):
        for e in self.__emprestimos:
            if e.getId() == id:
                return e
        return None

    def registrarDevolucao(self, idEmprestimo, data_devolucao):
        emprestimo = self.buscarPorId(idEmprestimo)
        if emprestimo is None:
            print("Empréstimo não encontrado.")
            return

        emprestimo.setDataDevolucao(data_devolucao)
        emprestimo.setStatus(StatusEmprestimo.DEVOLVIDO)

        for item in emprestimo.getItens():
            item.getLivro().devolverExemplar()

        atraso = (data_devolucao - emprestimo.getDataEmprestimo()).days - 7  
        #(TODO) Arrumar aqui
        print(emprestimo.getCliente())
        if atraso > 0:
            multa = Multa(str(uuid.uuid4()), atraso * 2.0, emprestimo, emprestimo.getCliente(), StatusMulta.PENDENTE)
            self.__multaController.addMulta(multa)
            emprestimo.getCliente().addMulta(multa)

        self.salvarEmprestimos()
        print(f"Empréstimo {idEmprestimo} devolvido com sucesso.")

    # ---------------- Persistência em arquivo ----------------
    def salvarEmprestimos(self):
        with open(self.__arquivo, "w", encoding="utf-8") as f:
            for e in self.__emprestimos:
                dataEmprestimo = e.getDataEmprestimo().isoformat() if e.getDataEmprestimo() else ""
                dataDevolucao = e.getDataDevolucao().isoformat() if e.getDataDevolucao() else ""
                multa_id = e.getMulta().getId() if e.getMulta() else ""
                itens_str = ",".join(str(i.getId()) for i in e.getItens()) if e.getItens() else ""
                f.write(f"{e.getId()};{e.getCliente().getId()};{dataEmprestimo};{dataDevolucao};{e.getStatus().name};{multa_id};{itens_str}\n")


    def carregarEmprestimos(self):
        if not os.path.exists(self.__arquivo):
            return
        from Model.Cliente import Cliente

        with open(self.__arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                dados = linha.strip().split(";")
                if len(dados) != 5:
                    continue
                id, idCliente, dataEmprestimo, dataDevolucao, status = dados
                cliente = self.__clienteController.buscarPorId(idCliente) if self.__clienteController else Cliente(idCliente, "", "", "")
                emprestimo = EmprestimoLivro(
                    id,
                    cliente,
                    date.fromisoformat(dataEmprestimo) if dataEmprestimo else None,
                    date.fromisoformat(dataDevolucao) if dataDevolucao else None,
                    StatusEmprestimo[status]
                )
                self.__emprestimos.append(emprestimo)

    # ---------------- Auxiliares ----------------
    def __garantirArquivo(self):
        os.makedirs(os.path.dirname(self.__arquivo), exist_ok=True)
        if not os.path.exists(self.__arquivo):
            with open(self.__arquivo, "w", encoding="utf-8"):
                pass
