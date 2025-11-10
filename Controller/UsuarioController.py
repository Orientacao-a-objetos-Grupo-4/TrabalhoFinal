import os
import pickle
from Model.Usuario import Usuario
from Untils.Enums import TipoUsuario
from Model.Cliente import Cliente
from Model.Funcionario import Funcionario

class UsuarioController:
    def __init__(self, arquivo="/Data/usuarios.txt"):
        self.__arquivo = arquivo
        self.__usuarios = self.__carregar_dados()

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

    def cadastrar_usuario(self, nomeUsuario, login, senha, tipo: TipoUsuario):
        novo_id = len(self.__usuarios) + 1

        if tipo == TipoUsuario.CLIENTE:
            usuario = Cliente(novo_id, nomeUsuario, login, senha)
        elif tipo == TipoUsuario.FUNCIONARIO:
            usuario = Funcionario(novo_id, nomeUsuario, login, senha)
        else:
            usuario = Funcionario(novo_id, nomeUsuario, login, senha)
      

        self.__usuarios.append(usuario)
        self.__salvar_dados()
        return usuario


    def listar_usuarios(self):
        return self.__usuarios

    def login(self, login, senha):
        for usuario in self.__usuarios:
            if usuario.getLogin() == login and usuario.getSenha() == senha:
                print(f"Login bem-sucedido! Bem-vindo, {usuario.getNomeUsuario()}")
                return usuario
        print("Login ou senha inválidos!")
        return None
