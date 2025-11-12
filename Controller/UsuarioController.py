import hashlib
import os
from Model.Usuario import Usuario
from Untils.Enums import TipoUsuario


class UsuarioController:
    def __init__(self, arquivo="Data/usuarios.txt"):
        self.__arquivo = arquivo
        os.makedirs(os.path.dirname(arquivo), exist_ok=True)
        self.__usuarios = self.__carregar_dados()
        self.__ultimo_id = self.__calcular_ultimo_id()


    def __carregar_dados(self):
        usuarios = []
        if os.path.exists(self.__arquivo):
            with open(self.__arquivo, "r", encoding="utf-8") as f:
                for linha in f:
                    usuario = Usuario.from_line(linha)
                    if usuario:
                        usuarios.append(usuario)
        return usuarios

    def __salvar_dados(self):
        with open(self.__arquivo, "w", encoding="utf-8") as f:
            for usuario in self.__usuarios:
                f.write(usuario.to_line())

    def __calcular_ultimo_id(self):
        if not self.__usuarios:
            return 0
        return max(usuario.getId() for usuario in self.__usuarios)
    
    def __hash_senha(self, senha):
        return hashlib.sha256(senha.encode()).hexdigest()

    def cadastrar_usuario(self, nomeUsuario, login, senha, tipo: TipoUsuario):
        """Cria e salva novo usuário"""
        if any(u.getLogin() == login for u in self.__usuarios):
            raise ValueError(f"Login '{login}' já está em uso!")

        self.__ultimo_id += 1
        senha = self.__hash_senha(senha)
        
        novo_usuario = Usuario.criar_usuario(
            self.__ultimo_id, nomeUsuario, login, senha, tipo
        )
        self.__usuarios.append(novo_usuario)
        self.__salvar_dados()
        return novo_usuario

    def listar_usuarios(self):
        return self.__usuarios

    def autenticar_usuario(self, login, senha):
        for usuario in self.__usuarios:
            if usuario.autenticar(login, senha):
                return usuario
        return None
