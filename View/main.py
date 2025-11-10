# main.py
import os
from datetime import date, timedelta

from Controller.UsuarioController import UsuarioController
from Controller.ClienteController import ClienteController
from Controller.FuncionarioController import FuncionarioController
from Controller.LivroController import LivroController
from Controller.ItensEmprestimoController import ItensEmprestimoController
from Controller.EmprestimoLivroController import EmprestimoLivroController
from Controller.MultaController import MultaController

from Untils.Enums import TipoUsuario, StatusEmprestimo, StatusMulta
from Model.ItensEmprestimo import ItensEmprestimo
from Model.EmprestimoLivro import EmprestimoLivro
from Model.Multa import Multa
from Model.Livro import Livro
from Model.Cliente import Cliente
from Model.Funcionario import Funcionario

# -------------------- Inicialização dos controllers --------------------
usuarioController = UsuarioController()
clienteController = ClienteController()
funcionarioController = FuncionarioController()
livroController = LivroController()
emprestimoController = EmprestimoLivroController()
itensController = ItensEmprestimoController(emprestimoController=emprestimoController)
multaController = MultaController(clienteController=clienteController, emprestimoController=emprestimoController)

# Setando controllers cruzados
emprestimoController.setClienteController(clienteController)
emprestimoController.setMultaController(multaController)
itensController.setEmprestimoController(emprestimoController)

# -------------------- Criando usuários --------------------
print("=== Criando Usuários ===")
cliente1 = usuarioController.cadastrar_usuario("João", "joao123", "senha123", TipoUsuario.CLIENTE)
funcionario1 = usuarioController.cadastrar_usuario("Maria", "maria123", "senha123",  TipoUsuario.FUNCIONARIO)

# Também adicionando explicitamente nos controllers específicos
clienteController.addCliente(cliente1)
funcionarioController.addFuncionario(funcionario1)

# -------------------- Criando livros --------------------
print("\n=== Criando Livros ===")
livro1 = Livro("L1", "Harry Potter", "Fantasia", "Rocco", "J.K. Rowling", 5)
livro2 = Livro("L2", "O Senhor dos Anéis", "Fantasia", "Martins", "J.R.R. Tolkien", 3)

livroController.addLivro(livro1)
livroController.addLivro(livro2)

# -------------------- Criando empréstimo --------------------
print("\n=== Criando Empréstimo ===")
data_hoje = date.today()
emprestimo1 = EmprestimoLivro("E1", cliente1, data_hoje)
emprestimoController.addEmprestimo(emprestimo1)
cliente1.addEmprestimo(emprestimo1)

# -------------------- Criando itens de empréstimo --------------------
print("\n=== Criando Itens de Empréstimo ===")
item1 = ItensEmprestimo("I1", livro1, emprestimo1)
item2 = ItensEmprestimo("I2", livro2, emprestimo1)
itensController.addItem(item1)
itensController.addItem(item2)
emprestimo1.addItem(item1)
emprestimo1.addItem(item2)

# Retirar exemplares dos livros
livro1.retirarExemplar()
livro2.retirarExemplar()

# -------------------- Registrando devolução com atraso e multa --------------------
print("\n=== Registrando Devolução com Atraso ===")
data_devolucao = data_hoje + timedelta(days=10)  # 3 dias de atraso
emprestimoController.registrarDevolucao("E1", data_devolucao)

# -------------------- Listando todos os dados --------------------
print("\n=== LISTAGEM DE USUÁRIOS ===")
for u in usuarioController.listar_usuarios():
    print(f"{u.getId()} - {u.getNomeUsuario()} ({u.getTipo().name})")

print("\n=== LISTAGEM DE CLIENTES ===")
for c in clienteController.getClientes():
    print(f"{c.getId()} - {c.getNomeUsuario()} - Empréstimos: {[e.getId() for e in c.getEmprestimos()]} - Multas: {[m.getId() for m in c.getMultas()]}")

print("\n=== LISTAGEM DE FUNCIONÁRIOS ===")
for f in funcionarioController.getFuncionarios():
    print(f"{f.getId()} - {f.getNomeUsuario()}")

print("\n=== LISTAGEM DE LIVROS ===")
for l in livroController.getLivros():
    print(f"{l.getId()} - {l.getTitulo()} - Exemplares disponíveis: {l.getNExemplares()}")

print("\n=== LISTAGEM DE EMPRÉSTIMOS ===")
for e in emprestimoController.getEmprestimos():
    print(f"{e.getId()} - Cliente: {e.getCliente().getNomeUsuario()} - Status: {e.getStatus().name} - Itens: {[i.getLivro().getTitulo() for i in e.getItens()]}")

print("\n=== LISTAGEM DE ITENS DE EMPRÉSTIMO ===")
for i in itensController.getItens():
    print(f"{i.getId()} - Livro: {i.getLivro().getTitulo()} - Empréstimo: {i.getEmprestimoLivro().getId()}")

print("\n=== LISTAGEM DE MULTAS ===")
for m in multaController.getMultas():
    print(f"{m.getId()} - Cliente: {m.getCliente().getNomeUsuario()} - Valor: {m.getValor():.2f} - Status: {m.getStatus().name}")
