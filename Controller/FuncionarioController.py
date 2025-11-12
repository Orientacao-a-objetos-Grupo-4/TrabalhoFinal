import os
from Model.Funcionario import Funcionario


class FuncionarioController:
    def __init__(self, arquivo="Data/funcionarios.txt"):
        self.__arquivo = arquivo
        self.__funcionarios = []
        self.carregarFuncionarios()

        if not os.path.exists(self.__arquivo):
            os.makedirs(os.path.dirname(self.__arquivo), exist_ok=True)
            open(self.__arquivo, "w", encoding="utf-8").close()

    # ------------------ CRUD ------------------

    def getFuncionarios(self):
        return self.__funcionarios

    def buscarPorId(self, id):
        return next((f for f in self.__funcionarios if f.getId() == id), None)

    def addFuncionario(self, funcionario):
        if self.buscarPorId(funcionario.getId()) is not None:
            print(f"Erro: Funcionário com ID {funcionario.getId()} já existe!")
            return False

        self.__funcionarios.append(funcionario)
        self.salvarFuncionarios()
        return True

    # ------------------ AÇÕES ------------------

    def cadastrarLivroPorFuncionario(self, funcionario_id, livroController, titulo, genero, editora, autor, n_exemplares):
        func = self.buscarPorId(funcionario_id)
        if not func:
            raise Exception("Funcionário não encontrado.")
        novo_livro = func.cadastrarLivro(livroController, titulo, genero, editora, autor, n_exemplares)
        if hasattr(livroController, "salvarLivros"):
            livroController.salvarLivros()
        return novo_livro

    def cadastrarClientePorFuncionario(self, funcionario_id, clienteController, usuarioController,nome, login, senha):
        func = self.buscarPorId(funcionario_id)
        if not func:
            raise Exception("Funcionário não encontrado.")
        novo_cliente = func.cadastrarCliente(clienteController,usuarioController,nome, login, senha)
        # garantir persistência
        if hasattr(clienteController, "salvarClientes"):
            clienteController.salvarClientes()
        return novo_cliente


    def registrarDevolucaoPorFuncionario(self, funcionario_id, emprestimoController, id_emprestimo):
        func = self.buscarPorId(funcionario_id)
        if not func:
            raise Exception("Funcionário não encontrado.")
        func.registrarDevolucao(emprestimoController, id_emprestimo)
        if hasattr(emprestimoController, "salvarEmprestimos"):
            emprestimoController.salvarEmprestimos()

    # ------------------ Persistência ------------------

    def carregarFuncionarios(self):
        if not os.path.exists(self.__arquivo):
            return

        with open(self.__arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                try:
                    partes = linha.strip().split(";")
                    if len(partes) != 5:
                        print(f"Linha inválida ignorada: {linha.strip()}")
                        continue

                    id_str, nome, login, senha, matricula = partes
                    funcionario = Funcionario(id_str, nome, login, senha, matricula)
                    self.__funcionarios.append(funcionario)
                except Exception as e:
                    print(f"Erro ao carregar funcionário: {linha.strip()} ({e})")

    def salvarFuncionarios(self):
        with open(self.__arquivo, "w", encoding="utf-8") as f:
            for func in self.__funcionarios:
                f.write(f"{func.getId()};{func.getNomeUsuario()};{func.getLogin()};{func.getSenha()};{func.getMatricula()}\n")
