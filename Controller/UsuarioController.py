import os
import pickle
import hashlib
import uuid
from Model.Usuario import Usuario
from Untils.Enums import TipoUsuario
from Model.Cliente import Cliente
from Model.Funcionario import Funcionario

class UsuarioController:
    def __init__(self, arquivo="Data/usuarios.txt"):
        self.__arquivo = arquivo
        self.__usuarios = self.__carregar_dados()
        self.__ultimo_id = self.__calcular_ultimo_id()

    # Carrega dados do arquivo pickle
    def __carregar_dados(self):
        if not os.path.exists(self.__arquivo):
            return []
        with open(self.__arquivo, "rb") as f:
            try:
                return pickle.load(f)
            except EOFError:
                return []

    def __salvar_dados(self):
        with open(self.__arquivo, "wb") as f:
            pickle.dump(self.__usuarios, f)

    def __calcular_ultimo_id(self):
        if not self.__usuarios:
            return 0
        return max(usuario.getId() for usuario in self.__usuarios)

    def __hash_senha(self, senha):
        return hashlib.sha256(senha.encode()).hexdigest()

    def cadastrar_usuario(self, nomeUsuario, login, senha, tipo: TipoUsuario):
        if any(u.getLogin() == login for u in self.__usuarios):
            raise ValueError(f"Login '{login}' já está em uso!")

        self.__ultimo_id += 1
        senha_hash = self.__hash_senha(senha)

        if tipo == TipoUsuario.CLIENTE:
            usuario = Cliente(self.__ultimo_id, nomeUsuario, login, senha_hash)
        elif tipo == TipoUsuario.FUNCIONARIO:
            matricula = uuid.uuid4()
            usuario = Funcionario(self.__ultimo_id, nomeUsuario, login, senha_hash,matricula=matricula)
        else:
            raise ValueError("Tipo de usuário inválido!")

        self.__usuarios.append(usuario)
        self.__salvar_dados()
        return usuario

    def listar_usuarios(self):
        return self.__usuarios.copy()

    def login(self, login, senha):
        senha_hash = self.__hash_senha(senha)
        for usuario in self.__usuarios:
            if usuario.getLogin() == login and usuario.getSenha() == senha_hash:
                return usuario
        return None
