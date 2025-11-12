from Untils.Enums import TipoUsuario


class Usuario:
    def __init__(self, id, nomeUsuario, login, senha, tipo: TipoUsuario):
        self.__id = id
        self.setNomeUsuario(nomeUsuario)
        self.setLogin(login)
        self.setSenha(senha)
        self.setTipo(tipo)

    # -----------------------------
    # Getters
    # -----------------------------
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
        """Converte o objeto para uma linha de texto."""
        return f"{self.__id};{self.__nomeUsuario};{self.__login};{self.__senha};{self.__tipo.name}\n"

    @staticmethod
    def from_line(line):
        """Cria um objeto Usuario a partir de uma linha de texto."""
        partes = line.strip().split(";")
        if len(partes) < 5:
            return None
        id = int(partes[0])
        nomeUsuario = partes[1]
        login = partes[2]
        senha = partes[3]
        tipo = TipoUsuario[partes[4]] 
        return Usuario(id, nomeUsuario, login, senha, tipo)

  
    @staticmethod
    def criar_usuario(id, nomeUsuario, login, senha, tipo: TipoUsuario):
        return Usuario(id, nomeUsuario, login, senha, tipo)

    def __str__(self):
        return f"[{self.__id}] {self.__nomeUsuario} ({self.__tipo.name})"
