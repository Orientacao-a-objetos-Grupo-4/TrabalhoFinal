

from Model.Usuario import Usuario
from Untils.Enums import TipoUsuario
import uuid



class Funcionario(Usuario):
    def __init__(self, id, nomeUsuario, login, senha, matricula):
        super().__init__(id, nomeUsuario, login, senha, TipoUsuario.FUNCIONARIO)
        self.__matricula = matricula

    # Getters e Setters
    def getMatricula(self):
        return self.__matricula

    def setMatricula(self, matricula):
        self.__matricula = matricula

    # Funções (exemplo)
    def cadastrarLivro(self, livroController, titulo, genero, editora, autor, n_exemplares):
        """Funcionário cadastra um novo livro."""
        from Model.Livro import Livro
        novo_livro = Livro(str(uuid.uuid4()), titulo, genero, editora, autor, n_exemplares)
        livroController.addLivro(novo_livro)
        return novo_livro

    def cadastrarCliente(self, clienteController,usuarioController ,nome, login, senha):
        """Funcionário cadastra um novo cliente."""
        from Model.Cliente import Cliente
        novo_cliente = clienteController.addCliente(Cliente.criar_usuario(str(uuid.uuid4()), nome, login, senha, TipoUsuario.CLIENTE))
        return novo_cliente

    def cadastrarEmprestimo(self, emprestimoController, cliente, itens):
        """Funcionário cria um novo empréstimo."""
        from datetime import date
        from Model.EmprestimoLivro import EmprestimoLivro
        emprestimo = EmprestimoLivro(str(uuid.uuid4()), cliente, date.today())
        for item in itens:
            emprestimo.addItem(item)
        emprestimoController.addEmprestimo(emprestimo)
        cliente.addEmprestimo(emprestimo)
        return emprestimo

    def registrarDevolucao(self, emprestimoController, id_emprestimo):
        """Funcionário registra devolução de um empréstimo."""
        from datetime import date
        emprestimoController.registrarDevolucao(id_emprestimo, date.today())