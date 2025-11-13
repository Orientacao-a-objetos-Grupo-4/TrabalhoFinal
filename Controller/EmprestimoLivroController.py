import os
from datetime import date
from Model.EmprestimoLivro import EmprestimoLivro

class EmprestimoLivroController:
    def __init__(self, arquivo="Data/emprestimos.txt", itensController=None, clienteController=None, multaController=None):
        self.__arquivo = arquivo
        self.__emprestimos = []
        self.__itensController = itensController
        self.__clienteController =  clienteController
        self.__multaController = multaController
        self.carregarEmprestimos()

        if not os.path.exists(self.__arquivo):
            os.makedirs(os.path.dirname(self.__arquivo), exist_ok=True)
            open(self.__arquivo, "w", encoding="utf-8").close()

    # -------- Setters de dependências --------
    def setItensController(self, itensController): self.__itensController = itensController
    def setClienteController(self, clienteController): self.__clienteController = clienteController
    def setMultaController(self, multaController): self.__multaController = multaController

    # -------- Métodos principais --------
    def getEmprestimos(self): return self.__emprestimos.copy()

    def addEmprestimo(self, emprestimo: EmprestimoLivro):
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

    def registrarDevolucao(self, idEmprestimo, data_devolucao):
        emprestimo = self.buscarPorId(idEmprestimo)
        if not emprestimo:
            print("Empréstimo não encontrado.")
            return

        multa = emprestimo.registrarDevolucao(data_devolucao)

        if multa and self.__multaController:
            self.__multaController.addMulta(multa)

        self.salvarEmprestimos()
        print(f"Empréstimo {idEmprestimo} devolvido com sucesso.")
        if multa:
            print(f"Multa gerada: R${multa.getValor():.2f}")

    # -------- Persistência --------
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
        with open(self.__arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                dados = linha.strip().split(";")
                if len(dados) < 5:
                    continue
                id, idCliente, dataEmprestimo, dataDevolucao, status = dados[:5]
                cliente = self.__clienteController.buscarPorId(idCliente) if self.__clienteController else Cliente(idCliente, "", "", "")
                emprestimo = EmprestimoLivro(
                    id,
                    cliente,
                    date.fromisoformat(dataEmprestimo) if dataEmprestimo else None,
                    date.fromisoformat(dataDevolucao) if dataDevolucao else None,
                )
                emprestimo.setStatus(status)
                self.__emprestimos.append(emprestimo)

    # -------- Métodos adicionais integrados --------
    def registrarDevolucao(self, idEmprestimo, dataDevolucao: date):
        emprestimo = self.buscarPorId(idEmprestimo)
        if not emprestimo:
            print("Empréstimo não encontrado!")
            return

        emprestimo.registrarDevolucao(dataDevolucao)
        self.salvarEmprestimos()

        dataPrevista = emprestimo.getDataDevolucao()  
        if dataPrevista and dataDevolucao > dataPrevista:
            diasAtraso = (dataDevolucao - dataPrevista).days
            if diasAtraso > 0:
                # Evita duplicar multa para o mesmo empréstimo
                multasExistentes = [m for m in self.__multaController.getMultas() if m.getEmprestimo().getId() == emprestimo.getId()]
                if not multasExistentes:
                    from Model.Multa import Multa
                    valor = diasAtraso * 0.1
                    multa = Multa(f"M-{emprestimo.getId()}", valor, emprestimo, emprestimo.getCliente())
                    self.__multaController.addMulta(multa)
