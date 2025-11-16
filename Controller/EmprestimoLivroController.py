import os
from datetime import date
from Model import Usuario
from Model.EmprestimoLivro import EmprestimoLivro

class EmprestimoLivroController:
    def __init__(self, arquivo="Data/emprestimos.txt", clienteController=None, multaController=None, livroController=None):
        self.__arquivo = arquivo
        self.__emprestimos = []
        self.__clienteController = clienteController
        self.__livroController = livroController
        self.__multaController = multaController

        # Corrigido: garantir existência do arquivo antes de carregar
        os.makedirs(os.path.dirname(arquivo), exist_ok=True)
        if not os.path.exists(arquivo):
            open(arquivo, "w", encoding="utf-8").close()

        self.carregarEmprestimos()

    # -------- Setters de dependências --------
    def setClienteController(self, clienteController): self.__clienteController = clienteController
    def setMultaController(self, multaController): self.__multaController = multaController
    def setLivroController(self, livroController): self.__livroController = livroController

    # -------- Métodos principais --------
    def getEmprestimos(self):
        return self.__emprestimos.copy()

    def addEmprestimo(self, emprestimo: EmprestimoLivro):
        self.__emprestimos.append(emprestimo)
        self.salvarEmprestimos()

    # RETIRADO: método getItens() pois empréstimo armazena itens, não o controller

    # -------- Busca itens dentro de um empréstimo --------
    def retornarItemPorId(self, idEmprestimo, idLivro):
        emprestimo = self.buscarPorId(idEmprestimo)
        if not emprestimo:
            return None

        for livro in emprestimo.getItens():
            if livro.getId() == idLivro:
                return livro

        return None

    def buscarporIdLivro(self, idEmprestimo):
        return self.buscarPorId(idEmprestimo)

    def verificarLivro(self, idLivro, idEmprestimo):
        emprestimo = self.buscarPorId(idEmprestimo)
        if not emprestimo:
            return False

        return any(livro.getId() == idLivro for livro in emprestimo.getItens())

    def removerEmprestimo(self, emprestimo):
        if emprestimo in self.__emprestimos:
            self.__emprestimos.remove(emprestimo)
            self.salvarEmprestimos()

    def buscarPorId(self, id):
        for e in self.__emprestimos:
            if e.getId() == id:
                return e
        return None

    # -------- Registrar devolução + multa --------
    def registrarDevolucao(self, idEmprestimo, dataDevolucao):
        emprestimo = self.buscarPorId(idEmprestimo)
        if not emprestimo:
            print("Empréstimo não encontrado.")
            return

        multa = emprestimo.registrarDevolucao(dataDevolucao)

        # Evita multa duplicada
        if multa and self.__multaController:
            multasExistentes = [
                m for m in self.__multaController.getMultas()
                if m.getEmprestimo().getId() == emprestimo.getId()
            ]
            if not multasExistentes:
                self.__multaController.addMulta(multa)

        self.salvarEmprestimos()

    # -------- Persistência --------
    def salvarEmprestimos(self):
        with open(self.__arquivo, "w", encoding="utf-8") as f:
            for e in self.__emprestimos:
                dataEmprestimo = e.getDataEmprestimo().isoformat() if e.getDataEmprestimo() else ""
                dataDevolucao = e.getDataDevolucao().isoformat() if e.getDataDevolucao() else ""
                multa_id = e.getMulta().getId() if e.getMulta() else ""
                itens_str = ",".join(str(i.getId()) for i in e.getItens()) if e.getItens() else ""

                f.write(
                    f"{e.getId()};"
                    f"{e.getCliente().getId()};"
                    f"{dataEmprestimo};"
                    f"{dataDevolucao};"
                    f"{e.getStatus().name};"
                    f"{multa_id};"
                    f"{itens_str}\n"
                )

    def carregarEmprestimos(self):
        if not os.path.exists(self.__arquivo):
            return

        with open(self.__arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                dados = linha.strip().split(";")
                if len(dados) < 5:
                    continue

                id, idCliente, dataEmprestimo, dataDevolucao, status = dados[:5]

                cliente = (
                    self.__clienteController.buscarPorId(idCliente)
                    if self.__clienteController
                    else Usuario(idCliente, "", "", "")
                )

                emprestimo = EmprestimoLivro(
                    id=id,
                    cliente=cliente,
                    dataEmprestimo=date.fromisoformat(dataEmprestimo) if dataEmprestimo else None,
                    dataDevolucao=date.fromisoformat(dataDevolucao) if dataDevolucao else None,
                )

                emprestimo.setStatus(status)

                # Carregar itens do empréstimo
                if len(dados) >= 7 and dados[6]:
                    itens_ids = dados[6].split(",")

                    for idLivro in itens_ids:
                        livro = self.__livroController.buscar_livro_por_id(idLivro)
                        if livro:
                            emprestimo.addItem(livro)

                self.__emprestimos.append(emprestimo)
