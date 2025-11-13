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
    def get_valor(self):
        return self.__valor

    def get_status(self):
        return self.__status

    def get_id(self):
        return self.__id

    def get_emprestimo(self):
        return self.__emprestimo

    def get_cliente(self):
        return self.__cliente

    def get_data_criacao(self):
        return self.__data_criacao

    # Setters with validation
    def set_valor(self, valor):
        if valor < 0:
            raise ValueError("Valor da multa não pode ser negativo")
        self.__valor = valor

    def set_status(self, status):
        if not isinstance(status, StatusMulta):
            raise ValueError("Status deve ser uma instância de StatusMulta")
        self.__status = status

    def calcular_valor(self):
        """Calcula o valor da multa baseado no atraso"""
        data_prevista = self.__emprestimo.get_data_prevista_devolucao()
        data_devolucao = self.__emprestimo.get_data_devolucao()

        if not data_prevista or not data_devolucao:
            self.set_valor(0.0)
            return

        if data_devolucao > data_prevista:
            dias_atraso = (data_devolucao - data_prevista).days
            valor_por_dia = 0.1
            self.set_valor(dias_atraso * valor_por_dia)
        else:
            self.set_valor(0.0)

    def registrar_pagamento(self):
        """Marca a multa como paga"""
        if self.__status == StatusMulta.PENDENTE:
            self.set_status(StatusMulta.PAGA)
            return True
        return False

    def esta_ativa(self):
        """Verifica se a multa está ativa (pendente)"""
        return self.__status == StatusMulta.PENDENTE

    @staticmethod
    def criar_multa(emprestimo, cliente, valor_inicial=0.0):
        """Factory method para criar multas"""
        if not emprestimo or not cliente:
            raise ValueError("Empréstimo e cliente são obrigatórios")
        
        try:
            id_multa = str(uuid.uuid4())
            return Multa(id_multa, valor_inicial, emprestimo, cliente)
        except Exception as e:
            raise Exception(f"Erro ao criar multa: {e}")

    def to_txt(self):
        return f"{self.get_id()};{self.get_valor()};{self.__emprestimo.get_id()};{self.__cliente.get_id()};{self.get_status().name}\n"

    def __str__(self):
        return f"Multa {self.__id} - Valor: R${self.__valor:.2f} - Status: {self.__status.name}"

    def to_dict(self):
        """Converte para dicionário (útil para views)"""
        return {
            'id': self.get_id(),
            'valor': self.get_id(),
            'status': self.get_status().name,
            'emprestimo_id': self.get_emprestimo().get_id(),
            'cliente_id': self.get_cliente().get_id(),
            'data_criacao': self.getdata_criacao().strftime("%d/%m/%Y %H:%M")
        }