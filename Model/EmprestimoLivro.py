
from Untils.Enums import StatusEmprestimo

#retirei o objeto livro porque ja tem na classe itensemprestimo, então o emprestimo contempla varios livros atraves dos itens

#retirei a lista de multas, pq o emprestimo pode ter no maximo uma multa vinculada

#aqui precisamos importar o StatusMulta? Ele não vai estar apenas na classe Multa?

class EmprestimoLivro:
    def __init__(self, id, cliente, dataEmprestimo, dataDevolucao, status: StatusEmprestimo = StatusEmprestimo.ATIVO):
        self.__id = id
        self.__cliente = cliente
        self.__dataEmprestimo = dataEmprestimo
        self.__dataDevolucao = dataDevolucao
        self.__status = status
        self.__multa = None
        self.__itens = []

    # Getters
    def getId(self):
        return self.__id

    def getCliente(self):
        return self.__cliente

    def getItens(self):
        return self.__itens

    def getDataEmprestimo(self):
        return self.__dataEmprestimo

    def getDataDevolucao(self):
        return self.__dataDevolucao

    def getStatus(self):
        return self.__status

    def getMulta(self):
        return self.__multa

    # Setters
    def setStatus(self, status):
        self.__status = status

    def setDataEmprestimo(self, dataEmprestimo):
        self.__dataEmprestimo = dataEmprestimo

    def setDataDevolucao(self, dataDevolucao):
        self.__dataDevolucao = dataDevolucao

    def setMulta(self, multa):
        self.__multa = multa

    # Métodos auxiliares
    
    def add_item(self, item_emprestimo):
        self.__itens.append(item_emprestimo)

    def calcularMullta(self):
        pass

    def registrarDevolucao(self, dataDevolucao):
        self.setDataDevolucao(dataDevolucao)
        self.setStatus(StatusEmprestimo.DEVOLVIDO)
     