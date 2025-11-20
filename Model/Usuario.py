# Model/Usuario.py
from datetime import date
import uuid
from Untils.Enums import TipoUsuario


class Usuario:
    def __init__(self, id, nomeUsuario, login, senha, tipo: TipoUsuario, multas=None, emprestimos=None):
        self.__id = id
        self.setNomeUsuario(nomeUsuario)
        self.setLogin(login)
        self.setSenha(senha)
        self.setTipo(tipo)
        self.__multas = multas if multas is not None else []
        self.__emprestimos = emprestimos if emprestimos is not None else []

    def getId(self):
        return self.__id

    def getNomeUsuario(self):
        return self.__nomeUsuario

    def getLogin(self):
        return self.__login

    def getSenha(self):
        return self.__senha

    def getTipo(self):
        return self.__tipo

    def getMultas(self):
        return self.__multas.copy()

    def getEmprestimos(self):
        return self.__emprestimos.copy()

    def setNomeUsuario(self, nomeUsuario):
        if not nomeUsuario or len(nomeUsuario.strip()) < 3:
            raise ValueError("O nome de usuário deve ter pelo menos 3 caracteres.")
        self.__nomeUsuario = nomeUsuario.strip()

    def setLogin(self, login):
        if not login or len(login.strip()) < 3:
            raise ValueError("O login deve ter pelo menos 3 caracteres.")
        self.__login = login.strip()

    def setSenha(self, senha):
        if not senha or len(senha) < 4:
            raise ValueError("A senha deve ter pelo menos 4 caracteres.")
        self.__senha = senha

    def setTipo(self, tipo):
        if not isinstance(tipo, TipoUsuario):
            raise ValueError("Tipo de usuário inválido.")
        self.__tipo = tipo

    def autenticar(self, login, senha):
        return self.__login == login and self.__senha == senha

    def to_line(self):
        multas_str = ",".join(str(m) for m in self.getMultas())
        emprestimos_str = ",".join(str(e) for e in self.getEmprestimos())
        return f"{self.getId()};{self.getNomeUsuario()};{self.getLogin()};{self.getSenha()};{self.getTipo().name};{multas_str};{emprestimos_str}\n"

    @staticmethod
    def from_line(line):
        partes = line.strip().split(";")
        if len(partes) < 5:
            return None
        id = partes[0]
        nomeUsuario = partes[1]
        login = partes[2]
        senha = partes[3]
        tipo = TipoUsuario[partes[4]]
        multas = []
        emprestimos = []
        if len(partes) > 5 and partes[5].strip():
            multas = [m for m in partes[5].split(",") if m.strip().isdigit()]
        if len(partes) > 6 and partes[6].strip():
            emprestimos = [e for e in partes[6].split(",") if e.strip().isdigit()]
        return Usuario(id, nomeUsuario, login, senha, tipo, multas, emprestimos)

    @staticmethod
    def criar_usuario(nomeUsuario, login, senha, tipo: TipoUsuario):
        return Usuario(str(uuid.uuid4()).replace("-", "")[:6], nomeUsuario, login, senha, tipo)

    def addEmprestimo(self, emprestimo):
        self.__emprestimos.append(emprestimo)

    def addMulta(self, multa):
        self.__multas.append(multa)

    

    def cadastrarUsuario(pessoaLogada, nome, login, senha, tipo: TipoUsuario):
        try:
            return Usuario.criar_usuario(nome, login, senha, tipo)
        except Exception as e:
            print(f"Erro: {e}")
            return None
