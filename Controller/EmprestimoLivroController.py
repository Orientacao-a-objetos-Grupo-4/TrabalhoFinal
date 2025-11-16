import os
from datetime import date
from Model import Usuario
from Model.EmprestimoLivro import EmprestimoLivro
from Untils.Enums import StatusEmprestimo


class EmprestimoLivroController:
    def __init__(self, arquivo="Data/emprestimos.txt", clienteController=None, multaController=None, livroController=None):
        self.__arquivo = arquivo
        self.__emprestimos = []
        self.__clienteController = clienteController
        self.__livroController = livroController
        self.__multaController = multaController

        os.makedirs(os.path.dirname(arquivo), exist_ok=True)
        if not os.path.exists(arquivo):
            open(arquivo, "w", encoding="utf-8").close()

        self.carregarEmprestimos()

    # -------- Setters --------
    def setClienteController(self, c):
        self.__clienteController = c

    def setMultaController(self, m):
        self.__multaController = m

    def setLivroController(self, l):
        self.__livroController = l

    # -------- Métodos principais --------
  

    def getEmprestimos(self):
        return self.__emprestimos.copy()

    def addEmprestimo(self, emprestimo: EmprestimoLivro):
        self.__emprestimos.append(emprestimo)
        self.salvarEmprestimos()

    def buscarPorId(self, id):
        for e in self.__emprestimos:
            if e.getId() == id:
                return e
        return None

    def retornarItemPorId(self, idEmprestimo, idLivro):
        emprestimo = self.buscarPorId(idEmprestimo)
        if not emprestimo:
            return None

        for item in emprestimo.getItens():
            if item.getLivro().getId() == idLivro:
                return item

        return None

    def verificarLivro(self, idLivro, idEmprestimo):
        emprestimo = self.buscarPorId(idEmprestimo)
        if not emprestimo:
            return False

        return any(item.getLivro().getId() == idLivro for item in emprestimo.getItens())

    def removerEmprestimo(self, emprestimo):
        if emprestimo in self.__emprestimos:
            self.__emprestimos.remove(emprestimo)
            self.salvarEmprestimos()

    # -------- Registrar devolução --------
    def registrarDevolucao(self, idEmprestimo, dataDevolucao):
        emprestimo = self.buscarPorId(idEmprestimo)
        if not emprestimo:
            print("Empréstimo não encontrado.")
            return

        multa = emprestimo.registrarDevolucao(dataDevolucao)

        # Evita duplicar multa
        if multa and self.__multaController:
            multas_existentes = [
                m for m in self.__multaController.getMultas()
                if m.getEmprestimo().getId() == emprestimo.getId()
            ]

            if not multas_existentes:
                self.__multaController.addMulta(multa)

        self.salvarEmprestimos()

    # -------- Persistência --------
    def salvarEmprestimos(self):
        with open(self.__arquivo, "w", encoding="utf-8") as f:
            for e in self.__emprestimos:
                dataEmprestimo = e.getDataEmprestimo().isoformat() if e.getDataEmprestimo() else ""
                dataPrevista = e.getDataPrevista().isoformat() if e.getDataPrevista() else ""
                multa_id = e.getMulta().getId() if e.getMulta() else ""
                itens_str = ",".join(str(i.getLivro().getId()) for i in e.getItens())

                f.write(
                    f"{e.getId()};"
                    f"{e.getCliente().getId()};"
                    f"{dataEmprestimo};"
                    f"{dataPrevista};"
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

                id, idCliente, dataEmprestimo, dataPrevista, status = dados[:5]

                cliente = (
                    self.__clienteController.buscar_por_id(idCliente)
                    if self.__clienteController
                    else Usuario(idCliente, "", "", "")
                )

                emprestimo = EmprestimoLivro(
                    id=id,
                    cliente=cliente,
                    dataEmprestimo=date.fromisoformat(dataEmprestimo) if dataEmprestimo else None,
                    dataPrevista=date.fromisoformat(dataPrevista) if dataPrevista else None,
                    status=StatusEmprestimo[status]
                )

                print(dados[5])


                # Carregar multa (índice 5)
                if len(dados) > 5 and dados[5]:
                    multa_id = dados[5]
                    multa = self.__multaController.buscarPorId(multa_id)
                    if multa:
                        emprestimo.setMulta(multa)

                # Carregar livros (índice 6)
                if len(dados) > 6 and dados[6]:
                    livros_ids = dados[6].split(",")
                    for idLivro in livros_ids:
                        livro = self.__livroController.buscarPorId(idLivro)
                        if livro:
                            emprestimo.addItem(livro)

                

                self.__emprestimos.append(emprestimo)
