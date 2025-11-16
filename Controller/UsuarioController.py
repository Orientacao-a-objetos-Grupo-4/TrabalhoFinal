import hashlib
import os
from Model.Usuario import Usuario
from Untils.Enums import TipoUsuario


class UsuarioController:
    def __init__(self, arquivo="Data/usuarios.txt"):
        self.arquivo = arquivo
        os.makedirs(os.path.dirname(arquivo), exist_ok=True)
        self.usuarios = self.carregar_dados()

    def carregar_dados(self):
        usuarios = []
        if os.path.exists(self.arquivo):
            with open(self.arquivo, "r", encoding="utf-8") as f:
                for linha in f:
                    usuario = Usuario.from_line(linha)
                    if usuario:
                        usuarios.append(usuario)
        return usuarios

    def salvar_dados(self):
        with open(self.arquivo, "w", encoding="utf-8") as f:
            for usuario in self.usuarios:
                f.write(usuario.to_line())

    def hash_senha(self, senha):
        return hashlib.sha256(senha.encode()).hexdigest()
    
    
    def cadastrar_adm(self, nome, login, senha, tipo: TipoUsuario):
        self.existe_login(login)
        senha_hash = self.hash_senha(senha)
        self.salvar_dados()

    def existe_login(self, login):
           if any(user.getLogin() == login for user in self.usuarios):
            raise ValueError(
                    f"O login '{login}' já existe. Por favor, escolha outro login."
                )
            print(f"Login '{login}' já está em uso!")


    def cadastrar_usuario(self,nomeUsuario, login, senha, tipo: TipoUsuario,pessoaLogada):
        senha_hash = self.hash_senha(senha)
        self.existe_login(login)
        novo_usuario = Usuario.cadastrarUsuario(nome=nomeUsuario, pessoaLogada=pessoaLogada,login=login, senha=senha_hash, tipo=tipo)
        self.usuarios.append(novo_usuario)
        self.salvar_dados()
        return novo_usuario

    def listar_usuarios(self):
        return self.usuarios

    def buscar_por_login(self, login):
        return next((u for u in self.usuarios if u.getLogin() == login), None)
    
    def buscar_por_id(self, id):
        return next((u for u in self.usuarios if u.getId() == id), None)

    def autenticar_usuario(self, login, senha):
        senha_hash = self.hash_senha(senha)
        for usuario in self.usuarios:
            if usuario.getLogin() == login and usuario.getSenha() == senha_hash:
                return usuario
        return None