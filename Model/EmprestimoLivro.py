import uuid
from Model.ItensEmprestimo import ItemEmprestimo
from Untils.Enums import StatusEmprestimo, StatusMulta
from datetime import date, timedelta
from Model.Multa import Multa

class EmprestimoLivro:
    def __init__(self, id, cliente, dataEmprestimo, dataPrevista, status: StatusEmprestimo = StatusEmprestimo.ATIVO):
        self.__id = id
        self.__cliente = cliente
        self.__dataEmprestimo = dataEmprestimo
        self.__dataPrevista = dataPrevista  
        self.__status = status
        self.__multa = None
        self.__livros = [] 

    # ---------------- Getters ----------------
    def getId(self):
        return self.__id

    def getCliente(self):
        return self.__cliente

    def getItens(self):
        return self.__livros

    def getDataEmprestimo(self):
        return self.__dataEmprestimo

    def getDataPrevista(self):  
        return self.__dataPrevista

    def getStatus(self):
        return self.__status

    def getMulta(self):
        return self.__multa

    # ---------------- Setters ----------------
    def setStatus(self, status):
        self.__status = status

    def setDataEmprestimo(self, dataEmprestimo):
        self.__dataEmprestimo = dataEmprestimo

    def setDataPrevista(self, dataPrevista):  # CORREÇÃO: mudado para setDataPrevista
        self.__dataPrevista = dataPrevista

    def setMulta(self, multa):
        self.__multa = multa

    def setLivros(self, livros):  
        self.__livros = livros

    # ---------------- Métodos auxiliares ----------------
    def addItem(self, livro):
        """Adiciona um item ao empréstimo."""
        self.__livros.append(livro)
        return livro

    def criarEmprestimo(cliente, livros, dataEmprestimo, dataPrevista):
        """Cria um novo empréstimo com os livros fornecidos."""
        emprestimo = EmprestimoLivro(
            id=str(uuid.uuid4()).replace("-", "")[:6],
            cliente=cliente,
            dataEmprestimo=dataEmprestimo,
            dataPrevista=dataPrevista
        )
        
        for livro in livros:
            emprestimo.addItem(livro)
            livro.retirarExemplar()

        return emprestimo

    def calcularAtraso(self, data_devolucao):
        """Calcula o número de dias de atraso."""
        dias = (data_devolucao - self.getDataPrevista()).days
        return dias if dias > 0 else 0

    def gerarMulta(self, dias_atraso):
        """Gera uma multa com base no atraso."""
        if dias_atraso <= 0:
            return None

        valor_multa = dias_atraso * 2.0
        multa = Multa(
            str(uuid.uuid4()).replace("-", "")[:6],
            valor_multa,
            self,
            self.__cliente,
            StatusMulta.PENDENTE
        )
        self.__multa = multa
        return multa

    def registrarDevolucao(self, data_devolucao: date):
        """Registra devolução e aplica multa se necessário."""
        self.setStatus(StatusEmprestimo.DEVOLVIDO)

        for item in self.__livros:
            item.devolverExemplar()

        dias_atraso = self.calcularAtraso(data_devolucao)
        return self.gerarMulta(dias_atraso)