import os
from datetime import date
from Controller.UsuarioController import UsuarioController
from Controller.ClienteController import ClienteController
from Controller.LivroController import LivroController
from Controller.EmprestimoLivroController import EmprestimoLivroController
from Controller.MultaController import MultaController
from Controller.ItensEmprestimoController import ItensEmprestimoController
from Model.Cliente import Cliente
from Model.Usuario import Usuario
from Model.Livro import Livro
from Model.EmprestimoLivro import EmprestimoLivro

# ---------------------
# Inicialização
# ---------------------
usuarioController = UsuarioController()
clienteController = ClienteController()
livroController = LivroController()
emprestimoController = EmprestimoLivroController()
multaController = MultaController(clienteController=clienteController, emprestimoController=emprestimoController)
itensEmprestimoController = ItensEmprestimoController(emprestimoController=emprestimoController)

emprestimoController.setItensController(itensEmprestimoController)
emprestimoController.setClienteController(clienteController)
emprestimoController.setMultaController(multaController)

# ---------------------
# Funções auxiliares
# ---------------------
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

def pausar():
    input("\nPressione ENTER para continuar...")

# ---------------------
# Menus
# ---------------------
def menu_principal():
    while True:
        limpar_tela()
        print("===== SISTEMA DE BIBLIOTECA =====")
        print("1 - Usuários")
        print("2 - Clientes")
        print("3 - Livros")
        print("4 - Empréstimos")
        print("5 - Multas")
        print("0 - Sair")

        opc = input("Escolha uma opção: ")

        if opc == "1":
            menu_usuarios()
        elif opc == "2":
            menu_clientes()
        elif opc == "3":
            menu_livros()
        elif opc == "4":
            menu_emprestimos()
        elif opc == "5":
            menu_multas()
        elif opc == "0":
            break
        else:
            print("Opção inválida!")
            pausar()

# ---------------------
# Menus específicos
# ---------------------
def menu_usuarios():
    limpar_tela()
    print("=== CADASTRO DE USUÁRIOS ===")
    nome = input("Nome: ")
    email = input("Email: ")
    senha = input("Senha: ")

    usuario = Usuario(nome=nome, email=email, senha=senha)
    usuarioController.cadastrar(usuario)
    print("Usuário cadastrado com sucesso!")
    pausar()

def menu_clientes():
    limpar_tela()
    print("=== CADASTRO DE CLIENTES ===")
    nome = input("Nome: ")
    cpf = input("CPF: ")

    cliente = Cliente(nome=nome, cpf=cpf)
    clienteController.addCliente(cliente)
    print("Cliente cadastrado com sucesso!")
    pausar()

def menu_livros():
    limpar_tela()
    print("=== CADASTRO DE LIVROS ===")
    titulo = input("Título: ")
    autor = input("Autor: ")
    ano = int(input("Ano: "))

    livro = Livro(titulo=titulo, autor=autor, ano=ano)
    livroController.addLivro(livro)
    print("Livro cadastrado com sucesso!")
    pausar()

def menu_emprestimos():
    limpar_tela()
    print("=== NOVO EMPRÉSTIMO ===")
    id_cliente = input("ID do cliente: ")
    cliente = clienteController.buscarPorId(id_cliente)

    if not cliente:
        print("Cliente não encontrado!")
        return pausar()

    id_livro = input("ID do livro: ")
    livro = livroController.buscarPorId(id_livro)

    if not livro:
        print("Livro não encontrado!")
        return pausar()

    emprestimo = EmprestimoLivro(cliente=cliente, dataEmprestimo=date.today())
    emprestimoController.addEmprestimo(emprestimo)
    itensEmprestimoController.adicionarItem(emprestimo, livro)
    print("Empréstimo realizado com sucesso!")
    pausar()

def menu_multas():
    limpar_tela()
    print("=== MULTAS ===")
    multas = multaController.getMultas()
    if not multas:
        print("Nenhuma multa registrada.")
    else:
        for m in multas:
            print(f"ID: {m.getId()} | Cliente: {m.getCliente().getNome()} | Valor: R${m.getValor():.2f} | Status: {m.getStatus().name}")
    pausar()

# ---------------------
# Execução principal
# ---------------------
if __name__ == "__main__":
    menu_principal()
