from Untils.Enums import StatusMulta


class Multa:
    def __init__(self, id, valor, emprestimo, cliente, status: StatusMulta = StatusMulta.PENDENTE):
        self.__id = id
        self.__valor = valor
        self.__status = status
        self.__emprestimo = emprestimo
        self.__cliente = cliente

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

    # Setters
    def setValor(self, valor):
        self.__valor = valor

    def setStatus(self, status):
        if isinstance(status, StatusMulta):
            self.__status = status
        else:
            print("Status inválido")
    
    def setEmprestimo(self, emprestimo):
        self.__emprestimo = emprestimo


    def setCliente(self, cliente):
        self.__cliente = cliente

    # Métodos auxiliares

    def calcularValor(self):
        dataEmprestimo = self.__emprestimo.getDataEmprestimo()
        dataDevolucao = self.__emprestimo.getDataDevolucao()
        diasAtraso = (dataDevolucao - dataEmprestimo).days
        if diasAtraso > 0:
            self.__valor = diasAtraso * 0.1
        else:
            self.__valor = 0

        data_prevista = self.getEmprestimo().getDataPrevistaDevolucao()
        data_devolucao = self.getEmprestimo().getDataDevolucao()

        if data_prevista and data_devolucao and data_devolucao > data_prevista:
            dias_atraso = (data_devolucao - data_prevista).days
            self.setValor(dias_atraso * valor_por_dia)
        else:
            self.setValor(0.0)  
    def registrarPagamento(self):
        """
        Marca a multa como paga.
        """
        if self.getStatus() == StatusMulta.PENDENTE:
            self.setStatus(StatusMulta.PAGA)  
        else:
            print(f"A multa {self.getId()} já está paga ou cancelada.")

    def to_txt(self):
        """
        Retorna uma linha formatada para salvar no arquivo.
        """
        return f"{self.getId()};{self.getValor()};{self.getEmprestimo().getId()};{self.getCliente().getId()};{self.getStatus().name}\n"