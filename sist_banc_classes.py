from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco # str
        self.contas = [] # list
    
    def realizar_transacao(self, conta, transacao): # conta, transacao
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def __str__(self):
        return f"Endereço:{self.endereco}\nContas:{self.contas}"

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.cpf = cpf # str
        self.nome = nome # str
        self.data_nascimento = data_nascimento # date

    def __str__(self):
        nums = []
        for i in self.contas:
            nums.append(i.numero)
        return f"\nNome: {self.nome}\nCPF: {self.cpf}\nEndereço: {self.endereco}\nContas: {nums}\nNascimento: {self.data_nascimento}"

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0.0 # float
        self._numero = numero # int
        self._agencia = "0001" # str
        self._cliente = cliente # Cliente
        self._historico = Historico() # Historico
    @classmethod
    def nova_conta(cls,cliente, numero):
        return cls(cliente,numero) # conta
    @property
    def saldo(self):
        return self._saldo
    @property
    def numero(self):
        return self._numero
    @property
    def agencia(self):
        return self._agencia
    @property
    def cliente(self):
        return self._cliente
    @property
    def historico(self):
        return self._historico
    
    
    def sacar(self, valor):
        if self.saldo > valor and valor > 0:
            self._saldo -= valor
            print("Saque feito com sucesso!")
            return True
        if valor > self.saldo:
            print("Saldo insuficiente!")
        if valor < 0:
            print("Informe um valor válido!")
        return False        
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito feito com sucesso!")
            return True
        print("Informe um valor válido!")
        return False
    
class ContaCorrente(Conta):
    def __init__(self, numero, cliente):
        super().__init__(numero, cliente)
        self.limite = 500
        self.limite_saques = 3
    def sacar(self, valor):
        #numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"]==Saque.__name__])
        numero_saques = len([transacao for transacao in self.historico.transacoes if "Saque" in transacao])        
        if self.limite_saques > numero_saques and self.limite > valor:
            return super().sacar(valor)
        if numero_saques > self.limite_saques:
            print("Limite de saques atingido!")
        if valor >= self.limite:
            print(f"O valor deve ser menor que R$ {self.limite:.2f}")
        return False        
                             
    def __str__(self):
        return f"\nNum: {self.numero}\nSaldo: {self.saldo}\nAgencia: {self.agencia}\nCliente: {self.cliente.cpf}\nHistorico: {self.historico.transacoes}"


class Historico:
    def __init__(self):
        self._transacoes = []
        pass
    @property
    def transacoes(self):
        return self._transacoes
    def adicionar_transacao(self, _transacao):
        self._transacoes.append(f"{_transacao.__class__.__name__}: R$ {_transacao.valor:.2f}")

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    @property
    def valor(self):
        return self._valor
    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    @property
    def valor(self):
        return self._valor
    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

def mostrar_valores(*objs):
    for obj in objs:
        print(obj)



menu = """
[1] Criar Pessoa
[2] Criar Conta
[3] Deposito
[4] Saque
[5] Mostrar usuários
[6] Mostrar contas
[7] Mostrar todos os usuários e contas
[0] Sair
=> """

def encontrar_pessoa(cpf, pessoas_total):
    for i in pessoas_total:
        if cpf == i.cpf:
            return i
    return None

def encontrar_conta(cliente, numero):
    for i in cliente.contas:
        if i.numero == numero:
            return i
    return None
        
def add_pessoa(endereco, cpf, nome, data_nascimento, pessoas_total):
    if encontrar_pessoa(cpf, pessoas_total) == None:
        pessoa_nova = PessoaFisica(endereco, cpf, nome, data_nascimento)
        pessoas_total.append(pessoa_nova)
        print("Pessoa registrada com sucesso!")
    else:
        print("Pessoa já registrada!")

def add_conta(cpf, numero, pessoas_total, contas_total):
    dono_da_conta_nova = encontrar_pessoa(cpf, pessoas_total)
    if dono_da_conta_nova == None:
        print("Pessoa não existe!")
    else:
        if encontrar_conta(dono_da_conta_nova, numero) == None:
            conta_nova = ContaCorrente(numero, dono_da_conta_nova)
            dono_da_conta_nova.adicionar_conta(conta_nova)
            contas_total.append(conta_nova)
            print(f"Conta '{numero}' criada com sucesso para {dono_da_conta_nova.nome}!")
        else:
            print(f"{dono_da_conta_nova.nome} já tem uma conta com o número '{numero}'!")

def mostrar_pessoas(pessoas_total):
    for i in pessoas_total:
        print(i)

def mostrar_contas(contas_total):
    for i in contas_total:
        print(i)

def motrar_pessoas_e_contas(pessoas_total):
    for i in pessoas_total:
        print("\nCLIENTE")
        print(i)
        print("\nCONTAS")
        for j in i.contas:
            print(j)

def deposito(cpf, pessoas_total, numero, valor):
    cliente = encontrar_pessoa(cpf, pessoas_total)
    if cliente != None:
        conta_do_cliente = encontrar_conta(cliente, numero)
        if conta_do_cliente != None:
            Deposito(valor).registrar(conta_do_cliente)
        else:
            print("Conta não encontrada!")
    else:
        print("Cliente não encontrado!")

def saque(cpf, pessoas_total, numero, valor):
    cliente = encontrar_pessoa(cpf, pessoas_total)
    if cliente != None:
        conta_do_cliente = encontrar_conta(cliente, numero)
        if conta_do_cliente != None:
            Saque(valor).registrar(conta_do_cliente)
        else:
            print("Conta não encontrada!")
    else:
        print("Cliente não encontrado!")

pessoas_total = []
contas_total = []


add_pessoa("Rua da Luz", "12345678901", "Gilberto", 1990-9-9, pessoas_total)
add_pessoa("Rua da Alegria", "34567890123", "Maria Clara", 2000-1-2, pessoas_total)
add_conta("12345678901", 1, pessoas_total, contas_total)
add_conta("12345678901", 2, pessoas_total, contas_total)
add_conta("34567890123", 1, pessoas_total, contas_total)

while True:
    op = int(input(menu))
    match op:
        case 1:
            print("ADICIONAR PESSOA")
            endereco = input("Endereço: ")
            cpf = input("CPF: ").replace('-','').replace('.','')
            nome = input("Nome: ")
            data_nascimento =[int(s) for s in input("Data de Nascimento(AAAA-MM-DD): ").split('-')]
            data_nascimento = datetime(data_nascimento[0], data_nascimento[1], data_nascimento[2]).date()
            add_pessoa(endereco, cpf, nome, data_nascimento, pessoas_total)
        case 2:
            print("ADICIONAR CONTA")
            cpf = input("CPF da pessoa que quer criar conta: ").replace('-','').replace('.','')
            numero = int(input("Número da conta: "))
            add_conta(cpf, numero, pessoas_total, contas_total)
        case 3:
            print("DEPÓSITO")
            cpf = input("CPF do dono da conta que deseja depositar: ")
            numero = int(input("Número da conta que deseja depositar: "))
            valor = float(input("Valor que deseja depositar: "))
            deposito(cpf, pessoas_total, numero, valor)
        case 4:
            print("SAQUE")
            cpf = input("CPF do dono da conta que deseja sacar: ")
            numero = int(input("Número da conta que deseja sacar: "))
            valor = float(input("Valor que deseja sacar: "))
            saque(cpf, pessoas_total, numero, valor)
        case 5:
            print("TODAS AS PESSOAS")
            mostrar_pessoas(pessoas_total)
        case 6:
            print("TODAS AS CONTAS")
            mostrar_contas(contas_total)
        case 7:
            print("TODAS AS PESSOAS E SUAS CONTAS")
            motrar_pessoas_e_contas(pessoas_total)