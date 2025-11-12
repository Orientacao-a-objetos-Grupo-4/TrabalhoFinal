from Controller.FuncionarioController import FuncionarioController
from Controller.ClienteController import ClienteController
from Controller.UsuarioController import UsuarioController
from Untils.Enums import TipoUsuario
from Model.Funcionario import Funcionario

# ------------------------
# Inicialização dos controllers
# ------------------------
usuarioController = UsuarioController()
funcionarioController = FuncionarioController()
clienteController = ClienteController()

# ------------------------
# 1️⃣ Criar um funcionário
# ------------------------
novo_funcionario = Funcionario(
    id="1",
    nomeUsuario="João Silva",
    login="joao.silva",
    senha="1234",
    matricula="FUNC001"
)

# Adiciona o funcionário e salva
funcionarioController.addFuncionario(novo_funcionario)
print("✅ Funcionário cadastrado e salvo com sucesso!")

# ------------------------
# 2️⃣ Funcionário cria um cliente
# ------------------------
funcionario_encontrado = funcionarioController.buscarPorId("1")
if funcionario_encontrado:
    novo_cliente = funcionario_encontrado.cadastrarCliente(
        clienteController=clienteController,
        usuarioController=usuarioController,
        nome="Maria Souza",
        login="maria.souza",
        senha="abcd"
    )
    print(f"✅ Cliente '{novo_cliente.getNomeUsuario()}' cadastrado com sucesso!")
else:
    print("❌ Funcionário não encontrado!")

# ------------------------
# 3️⃣ Listar todos para verificar
# ------------------------
print("\n📋 Funcionários cadastrados:")
for f in funcionarioController.getFuncionarios():
    print(f"ID: {f.getId()} | Nome: {f.getNomeUsuario()} | Matrícula: {f.getMatricula()}")

print("\n📋 Clientes cadastrados:")
for c in clienteController.getClientes():
    print(f"ID: {c.getId()} | Nome: {c.getNomeUsuario()} | Login: {c.getLogin()}")
