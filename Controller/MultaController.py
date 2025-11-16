import os
from Model.Multa import Multa
from Untils.Enums import StatusMulta

class MultaController:
    def __init__(self, arquivo="Data/multas.txt", clienteController=None, emprestimoController=None):
        self.__arquivo = arquivo
        self.__multas = []
        self.__clienteController = clienteController
        self.__emprestimoController = emprestimoController

        if not os.path.exists(os.path.dirname(self.__arquivo)):
            os.makedirs(os.path.dirname(self.__arquivo), exist_ok=True)
        if not os.path.exists(self.__arquivo):
            open(self.__arquivo, "w", encoding="utf-8").close()

        self.carregarMultas()

    def getMultas(self):
        return self.__multas
    
    def getMultasByUserId(self, idUsuario):
        """
        Retorna uma lista de objetos Multa associados ao ID de usuário fornecido.
        """
        # Garante que o ID do usuário seja tratado como string para comparação
        idUsuario_str = str(idUsuario).strip()
        
        multas_do_usuario = []
        
        for multa in self.__multas:
            # Garante que o objeto cliente existe antes de tentar acessar o ID
            cliente = multa.getCliente()
            
            if cliente and str(cliente.getId()) == idUsuario_str:
                multas_do_usuario.append(multa)
                
        return multas_do_usuario


    def criarMulta(self, valor, emprestimo, cliente):
        multa = Multa.criarMulta(emprestimo, cliente, valor)
        if multa:
            print("Multa criada com sucesso!")
            self.addMulta(multa)
            return multa
        print("Erro ao criar a multa.")
        return None

    def buscarPorId(self, id):
        for multa in self.__multas:
            if multa.getId() == id:
                return multa
        return None

    def addMulta(self, multa):
        self.__multas.append(multa)
        self.salvarMultas()

    def removerMulta(self, multa):
        if multa in self.__multas:
            self.__multas.remove(multa)
            self.salvarMultas()

    def removerPorId(self, id):
        multa = self.buscarPorId(id)
        if multa:
            self.__multas.remove(multa)
            self.salvarMultas()

    def calcularMulta(self, id):
        multa = self.buscarPorId(id)
        if multa:
            multa.calcularValor()
            self.salvarMultas()
            return multa.getValor()
        print("Multa não encontrada.")
        return 0.0

    def pagarMulta(self, id):
        multa = self.buscarPorId(id)
        if multa:
            multa.registrarPagamento()
            self.salvarMultas()
            print(f"Multa {id} paga com sucesso!")
        else:
            print("Multa não encontrada.")

    def salvarMultas(self):
    # 1. Abre o arquivo em modo de escrita ('w') para sobrescrever o conteúdo
        with open(self.__arquivo, "w", encoding="utf-8") as f:
            # 2. Itera sobre a lista de multas
            for multa in self.__multas:
                
                # Garante que os valores de referência existam para evitar erros
                emprestimo_id = multa.getEmprestimo().getId() if multa.getEmprestimo() else ""
                cliente_id = multa.getCliente().getId() if multa.getCliente() else ""
                
                # 3. Formata a linha de dados
                linha = (
                    f"{multa.getId()};"
                    f"{multa.getValor()};"  # Valor float
                    f"{emprestimo_id};"
                    f"{cliente_id};"
                    f"{multa.getStatus().name}\n" # Nome do Enum (PENDENTE, PAGA)
                )
                
                # 4. Escreve a linha no arquivo
                f.write(linha)


    def carregarMultas(self):
        if not os.path.exists(self.__arquivo):
            return
        
        from Model.Multa import Multa
        from Untils.Enums import StatusMulta

        self.__multas = [] 

        with open(self.__arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                dados = linha.strip().split(";")
                if len(dados) != 5:
                    continue

                id, valor, idEmprestimo, idCliente, status = dados

                try:
                    valor = float(valor)
                    status_enum = StatusMulta[status]
                except (ValueError, KeyError):
                    continue
                
                emprestimo = None
                if self.__emprestimoController:
                    emprestimo = self.__emprestimoController.buscarPorId(idEmprestimo)

                cliente = None
                if self.__clienteController:
                    cliente = self.__clienteController.buscar_por_id(idCliente)
                
                multa = Multa(
                    id=id,
                    valor=valor,
                    emprestimo=emprestimo,
                    cliente=cliente,
                    status=status_enum
                )
                
                self.__multas.append(multa)
                