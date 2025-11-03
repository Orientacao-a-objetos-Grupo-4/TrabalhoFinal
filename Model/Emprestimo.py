from enum import Enum


class EmprestimoLivro:
    def __init__(self, id, cliente, livro, dataEmprestimo, dataDevolucao,status = Enum("DEVOLVIDO", "ATIVO", "CANCELADO") ):
        self.__id = id
        self.__cliente = cliente
        self.__livro = livro
        self.__dataEmprestimo = dataEmprestimo
        self.__dataDevolucao = dataDevolucao
        self.__status = status
        self.__multa = []
        self.__cliente = None



    #Getters
    def getId(self):
        return self.__id
    
    def getLivro(self):
        return self.__livro
    
    def getCliente(self):
        return self.__cliente
    
    def getStatus(self):
        return self.__status
    
    def getMulta(self):
        return self.__multa
    
    def getDataEmprestimo(self):
        return self.__dataEmprestimo
    
    def getDataDevolucao(self):
        return self.__dataDevolucao
    
    
    #Setters

    def setStatus(self,status):
        self.__status = status

    def setMulta(self,multa):
        self.__multa = multa

    def setLivro(self,livro):
        self.__livro = livro

    def setCliente(self,cliente):
        self.__cliente = cliente

    def setDataEmprestimo(self,dataEmprestimo):
        self.__dataEmprestimo = dataEmprestimo

    def setDataDevolucao(self,dataDevolucao):
        self.__dataDevolucao = dataDevolucao

    def setId(self,id):
        self.__id = id

    

    #Untils

    def addMulta(self,multa):
        self.__multa.append(multa)

    def removeMulta(self,multa):
        self.__multa.remove(multa)

