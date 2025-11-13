from Controller.UsuarioController import UsuarioController
from Untils.Enums import TipoUsuario


def escolher_tipo_usuario(usuario_logado):
    tipos = list(TipoUsuario)
    print("\nTipos de usuário disponíveis:")

    for i, tipo in enumerate(tipos, start=1):
        print(f"{i} - {tipo.name}")

    try:
        opcao = int(input("Escolha o número do tipo de usuário: ").strip())
        if opcao < 1 or opcao > len(tipos):
            print("❌ Opção inválida! Escolha um número entre 1 e", len(tipos))
            return None

        tipo_escolhido = tipos[opcao - 1]

        if usuario_logado.getTipo() == TipoUsuario.FUNCIONARIO and tipo_escolhido != TipoUsuario.CLIENTE:
            print("⚠️ Funcionários só podem cadastrar clientes.")
            return None

        return tipo_escolhido
    except ValueError:
        print("❌ Digite um número válido.")
        return None


def menu_principal(usuario_logado, controller: UsuarioController):
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print(f"👤 Usuário logado: {usuario_logado.getNomeUsuario()} ({usuario_logado.getTipo().name})")
        print("1 - Cadastrar novo usuário")
        print("2 - Listar usuários")
        print("3 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome = input("Nome do novo usuário: ").strip()
            login = input("Login do novo usuário: ").strip()

            if controller.existe_login(login):
                print("⚠️ Esse login já está em uso. Escolha outro.")
                continue

            senha = input("Senha: ").strip()
            tipo = escolher_tipo_usuario(usuario_logado)
            if not tipo:
                continue

            try:
                novo = controller.cadastrar_usuario(
                    nomeUsuario=nome,
                    login=login,
                    senha=senha,
                    tipo=tipo,
                    pessoaLogada=usuario_logado
                )
                print(f"\n✅ Usuário '{novo.getNomeUsuario()}' cadastrado com sucesso!")
            except ValueError as e:
                print(f"❌ Erro ao cadastrar: {e}")

        elif opcao == "2":
            usuarios = controller.listar_usuarios()
            if not usuarios:
                print("📭 Nenhum usuário cadastrado.")
            else:
                print("\n=== Usuários Cadastrados ===")
                for u in usuarios:
                    print(f"{u.getId():<3} | {u.getNomeUsuario():<20} | {u.getTipo().name}")

        elif opcao == "3":
            print("👋 Saindo do sistema...")
            break

        else:
            print("❌ Opção inválida! Escolha entre 1 e 3.")


def menu_cliente(usuario_logado):
    while True:
        print("\n=== MENU DO CLIENTE ===")
        print(f"👤 Bem-vindo, {usuario_logado.getNomeUsuario()}!")
        print("1 - Consultar algo (em breve)")
        print("2 - Fazer algo (em breve)")
        print("3 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "3":
            print("👋 Saindo do menu do cliente...")
            break
        else:
            print("⚙️ Função ainda não disponível.")


def main():
    controller = UsuarioController()

    if not any(u.getTipo() == TipoUsuario.ADMINISTRADOR for u in controller.usuarios):
        print("⚙️ Nenhum administrador encontrado. Vamos criar o primeiro.")
        nome = input("Nome do administrador: ").strip()
        login = input("Login: ").strip()
        senha = input("Senha: ").strip()
        controller.cadastrar_adm(nome, login, senha, TipoUsuario.ADMINISTRADOR)
        print("✅ Administrador criado com sucesso!\n")

    print("=== LOGIN ===")
    login = input("Login: ").strip()
    senha = input("Senha: ").strip()
    usuario_logado = controller.autenticar_usuario(login, senha)

    if not usuario_logado:
        print("❌ Login ou senha incorretos.")
        return

    print(f"\n✅ Login realizado com sucesso! Bem-vindo, {usuario_logado.getNomeUsuario()}!")

    # Redireciona para o menu correto
    if usuario_logado.getTipo() == TipoUsuario.CLIENTE:
        menu_cliente(usuario_logado)
    else:
        menu_principal(usuario_logado, controller)


if __name__ == "__main__":
    main()
