class ItemEmprestimo:
    def __init__(self, livro):
        self._livro = livro

    def getId(self):
        return self._livro.getId()

    def getLivro(self):
        return self._livro
    