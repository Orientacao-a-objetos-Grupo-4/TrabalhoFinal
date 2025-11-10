from datetime import date, timedelta
import uuid
from Controller.ClienteController import ClienteController
from Controller.LivroController import LivroController
from Controller.EmprestimoLivroController import EmprestimoLivroController
from Controller.MultaController import MultaController
from Controller.ItensEmprestimoController import ItensEmprestimoController
from Model.Cliente import Cliente
from Model.Livro import Livro
from Model.EmprestimoLivro import EmprestimoLivro
from Model.ItensEmprestimo import ItensEmprestimo
from Untils.Enums import StatusEmprestimo

def main():
    clienteController = ClienteController()
    livroController = LivroController()
    emprestimoController = EmprestimoLivroController()
    multaController = MultaController()
    itensController = ItensEmprestimoController()

    # Setar referências para evitar circular import
    itensController.setEmprestimoController(emprestimoController)
    emprestimoController.setItensController(itensController)
    emprestimoController.setClienteController(clienteController)
    emprestimoController.setMultaController(multaController)

    # ----- Criar cliente e livros com UUID -----
    cliente_id = str(uuid.uuid4())
    cliente = Cliente(cliente_id, "Patrick", "patrick123", "senha123")
    clienteController.addCliente(cliente)

    livro1_id = str(uuid.uuid4())
    livro1 = Livro(livro1_id, "Python Avançado", "Tecnologia", "Editora A", "Autor X", 5)
    livroController.addLivro(livro1)

    livro2_id = str(uuid.uuid4())
    livro2 = Livro(livro2_id, "Aprenda Java", "Tecnologia", "Editora B", "Autor Y", 3)
    livroController.addLivro(livro2)

    livro3_id = str(uuid.uuid4())
    livro3 = Livro(livro3_id, "Aprenda Javascript", "Tecnologia", "Editora B", "Autor Y", 3)
    livroController.addLivro(livro3)

    # ----- Criar empréstimo e itens com UUID -----
    emprestimo_id = str(uuid.uuid4())
    emprestimo = EmprestimoLivro(
        emprestimo_id,
        cliente,
        date.today(),
        None,
        status=StatusEmprestimo.ATIVO
    )
    emprestimoController.addEmprestimo(emprestimo)
    cliente.addEmprestimo(emprestimo)

    item1 = ItensEmprestimo(str(uuid.uuid4()), livro1, emprestimo)
    item2 = ItensEmprestimo(str(uuid.uuid4()), livro2, emprestimo)
    itensController.addItem(item1)
    itensController.addItem(item2)

    # ----- Registrar devolução atrasada -----
    dataDevolucao = date.today() + timedelta(days=5)
    emprestimoController.registrarDevolucao(emprestimo_id, dataDevolucao)

    # ----- Mostrar multas -----
    for m in multaController.getMultas():
        print(f"Multa: {m.getId()}, Valor: {m.getValor()}, Cliente: {m.getCliente().getNomeUsuario()}")

if __name__ == "__main__":
    main()
