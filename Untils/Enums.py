from enum import Enum

class TipoUsuario(Enum):
    ADMINISTRADOR = "Administrador"
    CLIENTE = "Cliente"
    FUNCIONARIO = "Funcionário"


class StatusMulta(Enum):
    PAGA = "Paga"
    PENDENTE = "Pendente"
    CANCELADA = "Cancelada"


class StatusEmprestimo(Enum):
    DEVOLVIDO = "Devolvido"
    ATIVO = "Ativo"
    CANCELADO = "Cancelado"
