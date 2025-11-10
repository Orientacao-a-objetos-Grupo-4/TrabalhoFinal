import os
import uuid
from datetime import date, timedelta

from Controller.UsuarioController import UsuarioController
from Controller.ClienteController import ClienteController
from Controller.FuncionarioController import FuncionarioController
from Controller.LivroController import LivroController
from Controller.ItensEmprestimoController import ItensEmprestimoController
from Controller.EmprestimoLivroController import EmprestimoLivroController
from Controller.MultaController import MultaController

from Untils.Enums import TipoUsuario
from Model.ItensEmprestimo import ItensEmprestimo
from Model.EmprestimoLivro import EmprestimoLivro
from Model.Livro import Livro

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
emprestimoController.setItensController(itensController)
itensController.setEmprestimoController(emprestimoController)

# -------------------- Criando usuários --------------------
print("=== Criando Usuários ===")
cliente1 = usuarioController.cadastrar_usuario("João", "joao123", "senha123", TipoUsuario.CLIENTE)
funcionario1 = usuarioController.cadastrar_usuario("Maria", "maria123", "senha123", TipoUsuario.FUNCIONARIO)

clienteController.addCliente(cliente1)
funcionarioController.addFuncionario(funcionario1)

# -------------------- Criando livros --------------------
print("\n=== Criando Livros ===")
livro1 = Livro(str(uuid.uuid4()), "Harry Potter", "Fantasia", "Rocco", "J.K. Rowling", 5)
livro2 = Livro(str(uuid.uuid4()), "O Senhor dos Anéis", "Fantasia", "Martins", "J.R.R. Tolkien", 3)

livroController.addLivro(livro1)
livroController.addLivro(livro2)

print("\n=== Criando Empréstimo ===")
data_hoje = date.today()
emprestimo1 = EmprestimoLivro(str(uuid.uuid4()), cliente1, data_hoje)
emprestimoController.addEmprestimo(emprestimo1)
cliente1.addEmprestimo(emprestimo1)

print("\n=== Criando Itens de Empréstimo ===")
item1 = ItensEmprestimo(str(uuid.uuid4()), livro1, emprestimo1)
item2 = ItensEmprestimo(str(uuid.uuid4()), livro2, emprestimo1)


#(TODO) SIMPLIFICAR AQUI
itensController.addItem(item1)
itensController.addItem(item2)

emprestimo1.addItem(item1)
emprestimo1.addItem(item2)

print("\n=== Registrando Devolução com Atraso ===")
data_devolucao = data_hoje + timedelta(days=10)
emprestimoController.registrarDevolucao(emprestimo1.getId(), data_devolucao)

print("\n=== LISTAGEM DE USUÁRIOS ===")
for u in usuarioController.listar_usuarios():
    print(f"{u.getId()} - {u.getNomeUsuario()} ({u.getTipo().name})")

print("\n=== LISTAGEM DE CLIENTES ===")
for c in clienteController.getClientes():
    emprestimos_ids = [e.getId() for e in c.getEmprestimos()] if hasattr(c, "getEmprestimos") else []
    multas_ids = [m.getId() for m in c.getMultas()] if hasattr(c, "getMultas") else []
    print(f"{c.getId()} - {c.getNomeUsuario()} - Empréstimos: {emprestimos_ids} - Multas: {multas_ids}")

print("\n=== LISTAGEM DE FUNCIONÁRIOS ===")
for f in funcionarioController.getFuncionarios():
    print(f"{f.getId()} - {f.getNomeUsuario()}")

print("\n=== LISTAGEM DE LIVROS ===")
for l in livroController.getLivros():
    print(f"{l.getId()} - {l.getTitulo()} - Exemplares disponíveis: {l.getNExemplares()}")

print("\n=== LISTAGEM DE EMPRÉSTIMOS ===")
for e in emprestimoController.getEmprestimos():
    itens = [i.getLivro().getTitulo() for i in e.getItens()] if e.getItens() else []
    print(f"{e.getId()} - Cliente: {e.getCliente().getNomeUsuario()} - Status: {e.getStatus().name} - Itens: {itens}")

print("\n=== LISTAGEM DE ITENS DE EMPRÉSTIMO ===")
for i in itensController.getItens():
    print(f"{i.getId()} - Livro: {i.getLivro().getTitulo()} - Empréstimo: {i.getEmprestimoLivro().getId()}")

print("\n=== LISTAGEM DE MULTAS ===")
for m in multaController.getMultas():
    print(f"{m.getId()} - Cliente: {m.getCliente().getNomeUsuario()} - Valor: {m.getValor():.2f} - Status: {m.getStatus().name}")
