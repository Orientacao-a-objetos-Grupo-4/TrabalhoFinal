# view_cli.py
import uuid
from datetime import date, timedelta

from Untils.Assistants import date_emp_plus_days, uuid_from_maybe_string
from Untils.Enums import TipoUsuario
from Controller.UsuarioController import UsuarioController
from Controller.LivroController import LivroController
from Controller.EmprestimoLivroController import EmprestimoLivroController
from Controller.MultaController import MultaController



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
def menu_cliente(usuario, emprestimoController, livroController, multaController):
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
                emprestimos = emprestimoController.pegarEmprestimosPorUsuario(usuario.getId())
                if not emprestimos:
                    print("\nVocê não tem empréstimos.\n")
                else:
                    print("\n--- MEUS EMPRÉSTIMOS ---")
                    for e in emprestimos:
                        status_name = e.getStatus().name if e.getStatus() else "N/A"
                        devolucao = e.getDataPrevista().isoformat() if e.getDataPrevista() else "N/A"
                        print(f"ID {e.getId()} - Status: {status_name} - Devolução prevista: {devolucao}")

            elif op == "3":
                print("\n--- MINHAS MULTAS ---")
                
                # 🛑 CORREÇÃO: Usar o Controller para buscar multas pelo ID do cliente
                multas = multaController.getMultasByUserId(usuario.getId())
                
                if not multas:
                    print("Você não tem multas pendentes.")
                else:
                    for m in multas:
                        status_name = m.getStatus().name if m.getStatus() else "N/A"
                        print(f"ID {m.getId()} - Valor: R${m.getValor():.2f} - Status: {status_name}")
            
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
            print("1 - Cadastrar Usuário")
            print("2 - Cadastrar Livro")
            print("3 - Registrar Empréstimo")
            print("4 - Registrar Devolução")
            print("5 - Listar Livros")
            print("6 - Listar Empréstimos")
            print("7 - Listar Multas")
            print("8 - Listar Usuários")
            print("0 - Voltar / Sair")
            op = input("Escolha: ").strip()

            if op == "1":
                nome = input("Nome: ").strip()
                login = input("Login: ").strip()
                senha = input("Senha: ").strip()
                tipo_input = input("Tipo (CLIENTE, FUNCIONARIO): ").strip().upper()

                if tipo_input not in TipoUsuario.__members__:
                    print("Tipo inválido.")
                    continue

                tipo = TipoUsuario[tipo_input]
                novo = usuarioController.cadastrar_usuario(nome, login, senha, tipo, pessoaLogada)
                print(f"Usuário criado: {novo.getId()} - {novo.getNomeUsuario()}")

            elif op == "2":
                print("\n=== CADASTRAR LIVRO ===")
                try:
                    titulo = input("Título: ").strip()
                    if livroController.getLivroByTitulo(titulo) is not None:
                        livroController.addLivro(livroController.getLivroByTitulo(titulo))
                        print("Exemplar Adicionado com sucesso!")
                        print("Livro já cadastrado.")
                        
                    else:
                        genero = input("Gênero: ").strip()
                        editora = input("Editora: ").strip()
                        autor = input("Autor: ").strip()
                        n_exemplares = int(input("Quantidade de exemplares: ").strip())
                        novo = livroController.criarLivro(titulo, genero, editora, autor, n_exemplares)
                        print(f"Livro cadastrado: {novo.getId()} - {novo.getTitulo()}")
                except Exception as ex:
                    print(f"Erro ao cadastrar livro: {ex}")

            # -------------------- REGISTRAR EMPRÉSTIMO (com vários livros) --------------------
            elif op == "3":
                try:
                    id_login = input("ID do cliente: ").strip()
                    cliente = usuarioController.buscar_por_id(id_login)
                    print(cliente.getId())

                    if not cliente:
                        print("Cliente não encontrado pelo ID.")
                        continue

                    # Criar empréstimo
                    emprestimo_id = str(uuid.uuid4())
                    data_emp = date.today()
                    data_dev = date_emp_plus_days(data_emp, 7)

                    from Model.EmprestimoLivro import EmprestimoLivro
                    emprestimo = EmprestimoLivro(emprestimo_id, cliente, data_emp, data_dev)

                    print("\nDigite os IDs dos livros que deseja emprestar.")
                    print("Digite ENTER sem escrever nada para finalizar.\n")

                    livrosSelecionados = []
                    while True:
                        id_livro = input("ID do livro: ").strip()

                        if id_livro == "":
                            livrosSelecionados = []
                            break

                        if emprestimoController.validarClienteEmprestimo(cliente.getId(), id_livro):
                            print("Este cliente já possui este livro emprestado e não o devolveu.")
                            continue

                        livro = livroController.buscarPorId(uuid_from_maybe_string(id_livro))
                        if not livro:
                            livro = livroController.buscarPorId(id_livro)
                        
                        if not livro:
                            print("Livro não encontrado.")
                            continue

                        if livro:
                            if livro in livrosSelecionados:
                                print("Livro ja selecionado! Escolha outro")
                                continue
                            else:
                                livrosSelecionados.append(livro)

                        # Verificar se já está no empréstimo
                        if emprestimoController.verificarLivro(livro.getId(), emprestimo.getId()):
                            print("Este livro já foi adicionado ao empréstimo.")
                            continue

                        if not livroController.retirarExemplar(livro.getId()):
                            print("Não há exemplares disponíveis para este livro.")
                            continue
                        
            
                        emprestimo.addItem(livro)  
                        print(f"Livro '{livro.getTitulo()}' adicionado ao empréstimo.")

                    if len(emprestimo.getItens()) == 0:
                        print("Nenhum livro selecionado. Empréstimo cancelado.")
                        continue
               
                    # Registrar nos controllers
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
                    print("Livros:")
                    if  e.getItens().__len__() == 0:
                        print("Nenhum livro empréstimo.")
                    else:
                        print()
                        for i in e.getItens():
                            print(f"ID Livro: {i.getLivro().getId()} - Livro: {i.getLivro().getTitulo()}")
                    print("Multas:")
                    if not e.getMulta():
                        print("Nenhuma multa registrada.")
                    else:
                        print(f"ID Multa: {e.getMulta().getId()} - Valor: {e.getMulta().getValor()}")

            elif op == "7":
                multas = multaController.getMultas()
                print("\n--- MULTAS ---")
                for m in multas:
                    print(f"ID: {m.getId()} Cliente: {m.getCliente().getNomeUsuario()} - R${m.getValor():.2f} - Status: {m.getStatus().name}")

            elif op == "8":
                usuarios = usuarioController.listar_usuarios()
                print("\n--- USUÁRIOS ---")
                for u in usuarios:
                    print(f"{u.getId()} - {u.getNomeUsuario()} - {u.getTipo().name}")

            elif op == "0":
                break

            else:
                print("Opção inválida.")

        except Exception as e:
            print(f"Erro inesperado: {e}")

# -------------------- Inicialização --------------------
if __name__ == "__main__":
    usuarioController = UsuarioController()
    livroController = LivroController()
    multaController = MultaController(clienteController=usuarioController, emprestimoController=None)
    emprestimoController = EmprestimoLivroController(clienteController=usuarioController, multaController=multaController, livroController=livroController)

    multaController._MultaController__emprestimoController = emprestimoController  

    pessoaLogada = None
    while not pessoaLogada:
        pessoaLogada = tela_login(usuarioController)

    if pessoaLogada.getTipo() == TipoUsuario.CLIENTE:
        menu_cliente(pessoaLogada, emprestimoController, livroController, multaController)
    else:
        menu_funcionario(usuarioController, emprestimoController, livroController, pessoaLogada)

    print("Encerrando sistema. Até logo!")