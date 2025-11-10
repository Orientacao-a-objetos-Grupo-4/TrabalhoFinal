from datetime import date
from Controller.ClienteController import ClienteController
from Controller.LivroController import LivroController
from Controller.EmprestimoLivroController import EmprestimoLivroController
from Controller.MultaController import MultaController
from Controller.ItensEmprestimoController import ItensEmprestimoController
from Model.Cliente import Cliente
from Model.Livro import Livro
from Model.EmprestimoLivro import EmprestimoLivro
from Model.ItensEmprestimo import ItensEmprestimo
from Model.Multa import Multa
from Untils.Enums import StatusEmprestimo, StatusMulta

def main():
    # ----- Inicializa controllers -----
    clienteController = ClienteController()
    livroController = LivroController()
    emprestimoController = EmprestimoLivroController()
    multaController = MultaController()
    itensController = ItensEmprestimoController()

    # ----- Cadastrar um cliente -----
    cliente = Cliente(1, "Patrick", "patrick123", "senha123")
    clienteController.addCliente(cliente)

    # ----- Cadastrar livros -----
    livro1 = Livro(1, "Python Avançado", "Tecnologia", "Editora A", "Autor X", 5)
    livro2 = Livro("L2", "Aprenda Java", "Tecnologia", "Editora B", "Autor Y", 3)
    livroController.addLivro(livro1)
    livroController.addLivro(livro2)

    # ----- Criar empréstimo -----
    emprestimo = EmprestimoLivro(1, cliente, date.today(), None, StatusEmprestimo.PENDENTE)
    emprestimoController.addEmprestimo(emprestimo)
    cliente.addEmprestimo(emprestimo)

    # ----- Adicionar itens ao empréstimo -----
    item1 = ItensEmprestimo(1, livro1, 1, emprestimo)
    item2 = ItensEmprestimo(2, livro2, 1, emprestimo)
    itensController.addItem(item1)
    itensController.addItem(item2)

    # ----- Registrar devolução com atraso -----
    dataDevolucao = date.today().replace(day=date.today().day + 5)  # exemplo: 5 dias depois
    emprestimoController.registrarDevolucao(1, dataDevolucao)

    # ----- Consultar multas -----
    for multa in multaController.getMultas():
        print(f"Multa ID: {multa.getId()}, Valor: {multa.getValor()}, Status: {multa.getStatus().name}, Cliente: {multa.getCliente().getNomeUsuario()}")

    # ----- Listar clientes -----
    print("\nClientes cadastrados:")
    for c in clienteController.getClientes():
        print(f"{c.getId()} - {c.getNomeUsuario()}")

    # ----- Listar livros -----
    print("\nLivros cadastrados:")
    for l in livroController.getLivros():
        print(f"{l.getId()} - {l.getTitulo()} ({l.getNExemplares()} exemplares)")

if __name__ == "__main__":
    main()
