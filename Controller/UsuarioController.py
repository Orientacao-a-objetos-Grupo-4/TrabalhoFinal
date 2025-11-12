import os
import pickle
from Model.Usuario import Usuario
from Untils.Enums import TipoUsuario


class UsuarioController:
    def __init__(self, arquivo="Data/usuarios.txt"):
        self.__arquivo = arquivo
        self.__usuarios = self.__carregar_dados()
        self.__ultimo_id = self.__calcular_ultimo_id()

        # Garante que o diretório exista
        os.makedirs(os.path.dirname(arquivo), exist_ok=True)

 
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


    def cadastrar_usuario(self, nomeUsuario, login, senha, tipo: TipoUsuario):
        """Chama o model para criar usuário e salva"""
        if any(u.getLogin() == login for u in self.__usuarios):
            raise ValueError(f"Login '{login}' já está em uso!")

        self.__ultimo_id += 1
        novo_usuario = Usuario.criar_usuario(
            self.__ultimo_id, nomeUsuario, login, senha, tipo
        )

        self.__usuarios.append(novo_usuario)
        self.__salvar_dados()
        return novo_usuario

    def listar_usuarios(self):
        return self.__usuarios

    def autenticar_usuario(self, login, senha):
        """Chama o model para autenticar"""
        return Usuario.autenticar(login, senha, self.__usuarios)
