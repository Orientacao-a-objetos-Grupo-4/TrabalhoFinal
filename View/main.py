from Model.Funcionario import Funcionario
from Model.Cliente import Cliente
from Model.Livro import Livro
from Model.EmprestimoLivro import EmprestimoLivro
from Model.Multa import Multa
from Untils.Enums import StatusMulta, StatusEmprestimo

from datetime import date, timedelta


def main():
    print("===== SISTEMA DE BIBLIOTECA =====\n")

    # 1️⃣ Criar um funcionário
    funcionario = Funcionario("Ana Paula", "ana_admin", "1234", "FUNC001")
    print(f"Funcionário cadastrado: {funcionario.getNomeUsuario()} | Matrícula: {funcionario.getMatricula()}")

    # 2️⃣ Criar um cliente
    cliente = Cliente("João Silva", "joao123", "senha123")
    cliente.setCpf("123.456.789-10")
    print(f"Cliente cadastrado: {cliente.getNomeUsuario()} | CPF: {cliente.getCpf()}\n")

    # 3️⃣ Cadastrar um livro
    livro = Livro(1, "Dom Casmurro", "Romance", "Editora Clássica", "Machado de Assis", 3)
    print(f"Livro cadastrado: {livro.getTitulo()} ({livro.getNExemplares()} exemplares disponíveis)\n")

    # 4️⃣ Criar um empréstimo (pelo funcionário)
    data_emprestimo = date.today()
    data_devolucao = data_emprestimo + timedelta(days=7)

    emprestimo = EmprestimoLivro(
        id=101,
        cliente=cliente,
        livro=livro,
        dataEmprestimo=data_emprestimo,
        dataDevolucao=data_devolucao,
        status=StatusEmprestimo.ATIVO
    )

    cliente.addEmprestimo(emprestimo)
    livro.retirarExemplar()

    print(f"Empréstimo criado para {cliente.getNomeUsuario()}")
    print(f"Livro: {livro.getTitulo()}")
    print(f"Data de devolução: {emprestimo.getDataDevolucao()}")
    print(f"Exemplares restantes: {livro.getNExemplares()}\n")

    # 5️⃣ Gerar uma multa por atraso
    multa = Multa(id=501, valor=25.0, status=StatusMulta.PENDENTE)
    multa.setCliente(cliente)
    multa.addEmprestimo(emprestimo)

    cliente.addMulta(multa)
    emprestimo.addMulta(multa)

    print(f"💰 Multa gerada para {cliente.getNomeUsuario()} no valor de R$ {multa.getValor()}")
    print(f"Status da multa: {multa.getStatus().value}\n")

    # 6️⃣ Mostrar resumo final
    print("===== RESUMO FINAL =====")
    print(f"Cliente: {cliente.getNomeUsuario()}")
    print(f"Livros emprestados: {[emp.getLivro().getTitulo() for emp in cliente.getEmprestimos()]}")
    print(f"Multas pendentes: {len(cliente.getMultas())}")
    print(f"Status do empréstimo: {emprestimo.getStatus().value}")
    print(f"Status da multa: {multa.getStatus().value}")


if __name__ == "__main__":
    main()
