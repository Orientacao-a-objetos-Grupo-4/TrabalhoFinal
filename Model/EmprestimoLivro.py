import uuid
from Model import ItensEmprestimo
from Untils.Enums import StatusEmprestimo, StatusMulta
from datetime import date, timedelta
from Model.Multa import Multa

class EmprestimoLivro:
    def __init__(self, id, cliente, dataEmprestimo, dataDevolucao, status: StatusEmprestimo = StatusEmprestimo.ATIVO):
        self.__id = id
        self.__cliente = cliente
        self.__dataEmprestimo = dataEmprestimo
        self.__dataDevolucao = dataDevolucao
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

    def getDataDevolucao(self):
        return self.__dataDevolucao

    def getStatus(self):
        return self.__status

    def getMulta(self):
        return self.__multa

    # ---------------- Setters ----------------
    def setStatus(self, status):
        self.__status = status

    def setDataEmprestimo(self, dataEmprestimo):
        self.__dataEmprestimo = dataEmprestimo

    def setDataDevolucao(self, dataDevolucao):
        self.__dataDevolucao = dataDevolucao

    def setMulta(self, multa):
        self.__multa = multa

    def setLivrros(self,livro):
        self.__livros = livro


    # ---------------- Métodos auxiliares ----------------
    def addItem(self, livro):
        """Adiciona um item ao empréstimo."""
        from Model import ItensEmprestimo

        novo_item = ItensEmprestimo(
            id=str(len(self.__itens) + 1),
            emprestimoId=self.__id,
            livro=livro
        )
        self.__itens.append(novo_item)
        return novo_item




    def calcularAtraso(self, data_devolucao) :
        """Calcula o número de dias de atraso."""
        dias = (data_devolucao - self.getDataDevolucao()).days
        return dias if dias > 0 else 0

    def gerarMulta(self, dias_atraso):
        """Gera uma multa com base no atraso."""
        if dias_atraso <= 0:
            return None

        valor_multa = dias_atraso * 2.0
        multa = Multa(
            str(uuid.uuid4()),
            valor_multa,
            self,
            self.__cliente,
            StatusMulta.PENDENTE
        )
        self.__multa = multa
        self.__cliente.addMulta(multa)
        return multa
    
    

    def registrarDevolucao(self, data_devolucao: date):
        """Registra devolução e aplica multa se necessário."""
        self.setDataDevolucao(data_devolucao)
        self.setStatus(StatusEmprestimo.DEVOLVIDO)

        for item in self.__livros:
            item.getLivro().devolverExemplar()

        dias_atraso = self.calcularAtraso(data_devolucao)
        return self.gerarMulta(dias_atraso)