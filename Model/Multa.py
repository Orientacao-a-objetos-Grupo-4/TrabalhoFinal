# Código refatorado usando o padrão getId(), getValor(), etc.

import uuid
from datetime import datetime
from Untils.Enums import StatusMulta

class Multa:
    def __init__(self, id, valor, emprestimo, cliente, status: StatusMulta = StatusMulta.PENDENTE):
        self.__id = id
        self.__valor = valor
        self.__status = status
        self.__emprestimo = emprestimo
        self.__cliente = cliente
        self.__data_criacao = datetime.now()

    # Getters
    def getValor(self):
        return self.__valor

    def getStatus(self):
        return self.__status

    def getId(self):
        return self.__id

    def getEmprestimo(self):
        return self.__emprestimo

    def getCliente(self):
        return self.__cliente

    def getDataCriacao(self):
        return self.__data_criacao

    # Setters
    def setValor(self, valor):
        if valor < 0:
            raise ValueError("Valor da multa não pode ser negativo")
        self.__valor = valor

    def setStatus(self, status):
        if not isinstance(status, StatusMulta):
            raise ValueError("Status deve ser uma instância de StatusMulta")
        self.__status = status

    # Lógica
    def calcularValor(self):
        data_prevista = self.__emprestimo.getDataPrevistaDevolucao()
        data_devolucao = self.__emprestimo.getDataDevolucao()

        if not data_prevista or not data_devolucao:
            self.setValor(0.0)
            return

        if data_devolucao > data_prevista:
            dias_atraso = (data_devolucao - data_prevista).days
            valor_por_dia = 0.1
            self.setValor(dias_atraso * valor_por_dia)
        else:
            self.setValor(0.0)

    def registrarPagamento(self):
        if self.__status == StatusMulta.PENDENTE:
            self.setStatus(StatusMulta.PAGA)
            return True
        return False

    def estaAtiva(self):
        return self.__status == StatusMulta.PENDENTE

    @staticmethod
    def criarMulta(emprestimo, cliente, valor_inicial=0.0):
        if not emprestimo or not cliente:
            raise ValueError("Empréstimo e cliente são obrigatórios")

        id_multa = str(uuid.uuid4())
        return Multa(id_multa, valor_inicial, emprestimo, cliente)

    def toTxt(self):
        return f"{self.getId()};{self.getValor()};{self.__emprestimo.getId()};{self.__cliente.getId()};{self.getStatus().name}\n"

    def __str__(self):
        return f"Multa {self.__id} - Valor: R${self.__valor:.2f} - Status: {self.__status.name}"

    def toDict(self):
        return {
            'id': self.getId(),
            'valor': self.getValor(),
            'status': self.getStatus().name,
            'emprestimo_id': self.getEmprestimo().getId(),
            'cliente_id': self.getCliente().getId(),
            'data_criacao': self.getDataCriacao().strftime("%d/%m/%Y %H:%M")
        }