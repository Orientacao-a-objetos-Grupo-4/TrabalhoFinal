import uuid


class ItemEmprestimo:
    def __init__(self, livro, emprestimoId):
        self._id = str(uuid.uuid4()) 
        self._livro = livro
        self._emprestimoId = emprestimoId

    def getId(self):
        return self._id

    def getLivro(self):
        return self._livro

    def getEmprestimoId(self):
        return self._emprestimoId
