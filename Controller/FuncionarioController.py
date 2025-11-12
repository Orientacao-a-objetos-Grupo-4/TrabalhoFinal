import os
from Model.Funcionario import Funcionario


class FuncionarioController:
    def __init__(self, arquivo="Data/funcionarios.txt"):
        self.__arquivo = arquivo
        self.__funcionarios = []
        self.__garantir_arquivo()
        self.__carregar_funcionarios()

    # ---------------- Utilitários ----------------
    def __garantir_arquivo(self):
        os.makedirs(os.path.dirname(self.__arquivo), exist_ok=True)
        if not os.path.exists(self.__arquivo):
            open(self.__arquivo, "w", encoding="utf-8").close()

    # ---------------- CRUD ----------------
    def getFuncionarios(self):
        return self.__funcionarios.copy()

    def buscarPorId(self, id):
        return next((f for f in self.__funcionarios if f.getId() == id), None)

    def addFuncionario(self, funcionario):
        if self.buscarPorId(funcionario.getId()):
            print(f"Erro: Funcionário com ID {funcionario.getId()} já existe!")
            return False

        self.__funcionarios.append(funcionario)
        self.__salvar_funcionarios()
        return True

    
    def cadastrarLivroPorFuncionario(self, funcionario_id, livroController, titulo, genero, editora, autor, n_exemplares):
        func = self.buscarPorId(funcionario_id)
        if not func:
            raise Exception("Funcionário não encontrado.")
        return func.cadastrarLivro(livroController, titulo, genero, editora, autor, n_exemplares)

    def cadastrarClientePorFuncionario(self, funcionario_id, clienteController, usuarioController, nome, login, senha):
        func = self.buscarPorId(funcionario_id)
        if not func:
            raise Exception("Funcionário não encontrado.")
        return func.cadastrarCliente(clienteController, usuarioController, nome, login, senha)

    def registrarDevolucaoPorFuncionario(self, funcionario_id, emprestimoController, id_emprestimo):
        func = self.buscarPorId(funcionario_id)
        if not func:
            raise Exception("Funcionário não encontrado.")
        func.registrarDevolucao(emprestimoController, id_emprestimo)

    # ---------------- Persistência ----------------
    def __carregar_funcionarios(self):
        if not os.path.exists(self.__arquivo):
            return
        with open(self.__arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                try:
                    id_str, nome, login, senha, matricula = linha.strip().split(";")
                    func = Funcionario(id_str, nome, login, senha, matricula)
                    self.__funcionarios.append(func)
                except ValueError:
                    print(f"Linha inválida ignorada: {linha.strip()}")

    def __salvar_funcionarios(self):
        with open(self.__arquivo, "w", encoding="utf-8") as f:
            for func in self.__funcionarios:
                f.write(f"{func.getId()};{func.getNomeUsuario()};{func.getLogin()};{func.getSenha()};{func.getMatricula()}\n")
