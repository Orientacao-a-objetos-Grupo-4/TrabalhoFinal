# view_cli.py
import uuid
from datetime import date, timedelta

from Untils.Enums import TipoUsuario
from Controller.UsuarioController import UsuarioController
from Controller.LivroController import LivroController
from Controller.EmprestimoLivroController import EmprestimoLivroController
from Controller.MultaController import MultaController


class ItemEmprestimo:
    def __init__(self, livro):
        self._livro = livro

    def getId(self):
        return self._livro.getId()

    def getLivro(self):
        return self._livro
    

usuarioLogado = None

# -------------------- Telas / Menus --------------------
def tela_login(usuarioController):
    try:
        print("=== LOGIN ===")
        login = input("Login: ").strip()
        senha = input("Senha: ").strip()
        usuario = usuarioController.autenticar_usuario(login, senha)
        if usuario:
            print(f"\nBem-vindo, {usuario.getNomeUsuario()}! ({usuario.getTipo().name})\n")
            return usuario
        else:
            print("\nLogin ou senha incorretos!\n")
            return None
    except Exception as e:
        print(f"Erro no login: {e}")
        return None


# -------------------- MENU CLIENTE --------------------
def menu_cliente(usuario, emprestimoController, livroController):
    while True:
        try:
            print("\n=== MENU CLIENTE ===")
            print("1 - Listar Livros")
            print("2 - Listar Meus Empréstimos")
            print("3 - Listar Minhas Multas")
            print("4 - Pagar Multa (se houver)")
            print("0 - Voltar / Sair")
            op = input("Escolha: ").strip()

            if op == "1":
                livros = livroController.getLivros()
                print("\n--- LIVROS DISPONÍVEIS ---")
                for l in livros:
                    print(f"{l.getId()} - {l.getTitulo()} - Exemplares: {l.getNExemplares()}")

            elif op == "2":
                emprestimos = usuario.getEmprestimos()
                if not emprestimos:
                    print("\nVocê não tem empréstimos.\n")
                else:
                    print("\n--- MEUS EMPRÉSTIMOS ---")
                    for e in emprestimos:
                        status_name = e.getStatus().name if e.getStatus() else "N/A"
                        devolucao = e.getDataDevolucao().isoformat() if e.getDataDevolucao() else "N/A"
                        print(f"ID {e.getId()} - Status: {status_name} - Devolução prevista: {devolucao}")

            elif op == "3":
                print("\n--- MINHAS MULTAS ---")
                multas = usuario.getMultas()
                for m in multas:
                    print(f"ID {m.getId()} - Valor: R${m.getValor()}")
            
            elif op == "4":
                id_multa = input("ID da multa: ").strip()
                multaController.pagarMulta(id_multa)

            elif op == "0":
                break

            else:
                print("Opção inválida, tente novamente.")
        except Exception as e:
            print(f"Erro: {e}")


# -------------------- MENU FUNCIONÁRIO --------------------
def menu_funcionario(usuarioController, emprestimoController, livroController, pessoaLogada):
    while True:
        try:
            print("\n=== MENU FUNCIONÁRIO ===")
            print("1 - Cadastrar Cliente")
            print("2 - Cadastrar Livro")
            print("3 - Registrar Empréstimo")
            print("4 - Registrar Devolução")
            print("5 - Listar Livros")
            print("6 - Listar Empréstimos")
            print("0 - Voltar / Sair")
            op = input("Escolha: ").strip()

            if op == "1":
                try:
                    nome = input("Nome do cliente: ").strip()
                    login = input("Login: ").strip()
                    senha = input("Senha: ").strip()
                    novo = usuarioController.cadastrar_usuario(nome, login, senha, TipoUsuario.CLIENTE, pessoaLogada)
                    if novo:
                        print(f"Cliente cadastrado: {novo.getId()} - {novo.getNomeUsuario()}")
                    else:
                        print("Não foi possível cadastrar cliente.")
                except Exception as ex:
                    print(f"Erro ao cadastrar cliente: {ex}")

            elif op == "2":
                print("\n=== CADASTRAR LIVRO ===")
                try:
                    titulo = input("Título: ").strip()
                    autor = input("Autor: ").strip()
                    editora = input("Editora: ").strip()
                    livroController.cadastrar_livro(titulo, autor, editora)
                    print("Livro cadastrado com sucesso!")
                except Exception as ex:
                    print(f"Erro ao cadastrar livro: {ex}")

            # -------------------- REGISTRAR EMPRÉSTIMO (com vários livros) --------------------
            elif op == "3":
                try:
                    id_login = input("ID do cliente: ").strip()
                    cliente = usuarioController.buscar_por_login(id_login)
                    if not cliente:
                        print("Cliente não encontrado pelo login.")
                        continue

                    # Criar empréstimo vazio
                    emprestimo_id = str(uuid.uuid4())
                    data_emp = date.today()
                    data_dev = date_emp_plus_days(data_emp, 7)

                    from Model.EmprestimoLivro import EmprestimoLivro
                    emprestimo = EmprestimoLivro(emprestimo_id, cliente, data_emp, data_dev)

                    print("\nDigite os IDs dos livros que deseja emprestar.")
                    print("Digite ENTER sem escrever nada para finalizar.\n")

                    while True:
                        id_livro = input("ID do livro: ").strip()

                        if id_livro == "":
                            break

                        livro = livroController.buscarPorId(uuid_from_maybe_string(id_livro))
                        if not livro:
                            livro = livroController.buscarPorId(id_livro)

                        if not livro:
                            print("Livro não encontrado.")
                            continue

                        if not livroController.retirarExemplar(livro.getId()):
                            print("Não há exemplares disponíveis para este livro.")
                            continue

                        item = ItemEmprestimo(livro)
                        emprestimo.addItem(item)

                        print(f"Livro '{livro.getTitulo()}' adicionado ao empréstimo.")

                    if len(emprestimo.getItens()) == 0:
                        print("Nenhum livro selecionado. Empréstimo cancelado.")
                        continue

                    emprestimoController.addEmprestimo(emprestimo)
                    cliente.addEmprestimo(emprestimo)

                    print(f"\nEmpréstimo criado com sucesso!")
                    print(f"ID: {emprestimo.getId()}")
                    print(f"Livros emprestados: {len(emprestimo.getItens())}")

                except Exception as ex:
                    print(f"Erro ao registrar empréstimo: {ex}")

            elif op == "4":
                try:
                    id_emp = input("ID Empréstimo: ").strip()
                    emprestimoController.registrarDevolucao(id_emp, date.today())
                    print("Operação registrada.")
                except Exception as ex:
                    print(f"Erro ao registrar devolução: {ex}")

            elif op == "5":
                livros = livroController.getLivros()
                print("\n--- LIVROS ---")
                for l in livros:
                    print(f"{l.getId()} - {l.getTitulo()} - Exemplares: {l.getNExemplares()}")

            elif op == "6":
                emprestimos = emprestimoController.getEmprestimos()
                print("\n--- EMPRÉSTIMOS ---")
                for e in emprestimos:
                    cliente_nome = e.getCliente().getNomeUsuario()
                    print(f"{e.getId()} - Cliente: {cliente_nome} - Status: {e.getStatus().name}")

            elif op == "0":
                break

            else:
                print("Opção inválida.")

        except Exception as e:
            print(f"Erro inesperado: {e}")


# -------------------- MENU ADMIN --------------------
def menu_admin(usuarioController, livroController, emprestimoController, multaController):
    while True:
        try:
            print("\n=== MENU ADMINISTRADOR ===")
            print("1 - Cadastrar Usuário")
            print("2 - Cadastrar Livro")
            print("3 - Listar Livros")
            print("4 - Listar Usuários")
            print("5 - Listar Empréstimos")
            print("6 - Listar Multas")
            print("0 - Voltar / Sair")
            op = input("Escolha: ").strip()

            if op == "1":
                nome = input("Nome: ").strip()
                login = input("Login: ").strip()
                senha = input("Senha: ").strip()
                tipo_input = input("Tipo (CLIENTE, FUNCIONARIO, ADMINISTRADOR): ").strip().upper()

                if tipo_input not in TipoUsuario.__members__:
                    print("Tipo inválido.")
                    continue

                tipo = TipoUsuario[tipo_input]
                novo = usuarioController.cadastrar_usuario(nome, login, senha, TipoUsuario.name, pessoaLogada)
                print(f"Usuário criado: {novo.getId()} - {novo.getNomeUsuario()}")

            elif op == "2":
                titulo = input("Título: ").strip()
                genero = input("Gênero: ").strip()
                editora = input("Editora: ").strip()
                autor = input("Autor: ").strip()
                n_exemplares = int(input("Número de exemplares: ").strip())

                livro = livroController.criarLivro(titulo, genero, editora, autor, n_exemplares)
                print(f"Livro criado: {livro.getId()} - {livro.getTitulo()}")

            elif op == "3":
                livros = livroController.getLivros()
                print("\n--- LIVROS ---")
                for l in livros:
                    print(f"{l.getId()} - {l.getTitulo()} - Exemplares: {l.getNExemplares()}")

            elif op == "4":
                usuarios = usuarioController.listar_usuarios()
                print("\n--- USUÁRIOS ---")
                for u in usuarios:
                    print(f"{u.getId()} - {u.getNomeUsuario()} - {u.getTipo().name}")

            elif op == "5":
                emprestimos = emprestimoController.getEmprestimos()
                print("\n--- EMPRÉSTIMOS ---")
                for e in emprestimos:
                    print(f"{e.getId()} - Cliente: {e.getCliente().getNomeUsuario()} - Status: {e.getStatus().name}")

            elif op == "6":
                multas = multaController.getMultas()
                print("\n--- MULTAS ---")
                for m in multas:
                    print(f"{m.getId()} - R${m.getValor():.2f} - Status: {m.getStatus().name}")

    

            elif op == "0":
                break

            else:
                print("Opção inválida.")

        except Exception as e:
            print(f"Erro inesperado: {e}")


# -------------------- Helpers --------------------
def uuid_from_maybe_string(s):
    import uuid
    try:
        return uuid.UUID(s)
    except:
        return s


def date_emp_plus_days(dt, days):
    return dt + timedelta(days=days)


# -------------------- Inicialização --------------------
if __name__ == "__main__":
    usuarioController = UsuarioController()
    livroController = LivroController()
    multaController = MultaController(clienteController=usuarioController, emprestimoController=None)
    emprestimoController = EmprestimoLivroController(itensController=None, clienteController=usuarioController, multaController=multaController)

    multaController._MultaController__emprestimoController = emprestimoController  

    pessoaLogada = None
    while not pessoaLogada:
        pessoaLogada = tela_login(usuarioController)

    if pessoaLogada.getTipo() == TipoUsuario.CLIENTE:
        menu_cliente(pessoaLogada, emprestimoController, livroController)
    elif pessoaLogada.getTipo() == TipoUsuario.FUNCIONARIO:
        menu_funcionario(usuarioController, emprestimoController, livroController, pessoaLogada)
    elif pessoaLogada.getTipo() == TipoUsuario.ADMINISTRADOR:
        menu_admin(usuarioController, livroController, emprestimoController, multaController)

    print("Encerrando sistema. Até logo!")
