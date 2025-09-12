menu = """
[1] Depositar
[2] Sacar
[3] Extrato
[4] Criar usuário
[5] Criar conta corrente
[6] Mostrar usuários e contas
[0] Sair
=> """

def deposito(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
    else:
        print("Informe um valor válido")
    return saldo, extrato

def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):   
    if numero_saques == limite_saques:
        print("Limite de saques atingido!")
    if valor > limite:
        print("O valor deve ser menor que R$ 500.00")
    if valor > 0 and saldo >= valor:
        numero_saques += 1
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
    else:
        print("Valor inválido!")
    return saldo, extrato, numero_saques

def mostrar_extrato(saldo, /, *, extrato):
    print("EXTRATO")
    if extrato == "":
        print("Não foram realizadas movimentações")
    else:
        print(extrato)
        print(f"Saldo: R$ {saldo:.2f}")

def criar_usuario(cpf,nome,data_nascimento,endereco,usuarios):
    for i in usuarios:
        if cpf == i.get('cpf'):
            print("CPF já registrado!")
            return
    novo_usuario = dict(cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco)
    usuarios.append(novo_usuario)
    return

def criar_conta(agencia, num_conta, usuarios,contas):
    cpf = input("Diga o CPF do usuario que vai criar esta conta: ").replace('-','').replace('.','')
    for i in usuarios:
        if cpf == i.get('cpf'):
            nova_conta = dict(agencia=agencia, num_conta=num_conta, usuario=i)
            contas.append(nova_conta)
            num_conta += 1
            return num_conta
    print("Usuario ainda não registrado!")
    return num_conta

def mostrar_usuarios_e_contas(usuarios, contas):
    print("USUARIOS")
    if not usuarios:
        print("Nenhum usuário criado!")
    else:
        for i in usuarios:
            print(f"\nCPF: {i.get('cpf')}\nNome: {i.get('nome')}\nData de nascimento: {i.get('data_nascimento')}\nEndereço: {i.get('endereco')}")
            print("CONTAS:")
            for j in contas:
                if j.get('usuario').get('cpf') == i.get('cpf'):
                    print(f"Numero da conta: {j.get('num_conta')}\nAgencia: {j.get('agencia')}")


saldo = 0
limite = 500
extrato = ""
n_saques = 0
LIMITE_SAQUES = 3
AGENCIA = "0001"

usuarios = list()
contas = list()
num_conta = 1

while True:
    op = int(input(menu))
    if op == 1:
        valor = float(input("Diga o valor a ser depositado: "))
        saldo, extrato = deposito(saldo, valor, extrato)
    elif op == 2:
        valor = float(input("Informe o valor do saque: "))
        saldo, extrato, n_saques = saque(saldo=saldo, valor=valor, extrato=extrato, limite=limite,
                               numero_saques=n_saques, limite_saques=LIMITE_SAQUES)
    elif op == 3:
        mostrar_extrato(saldo, extrato=extrato)
    elif op == 4:
        cpf = input("CPF: ").replace('-','').replace('.','')
        nome = input("Nome: ")
        data_nascimento = input("Data de nascimento DD/MM/AAAA: ")
        endereco = input("Endereço: ")
        criar_usuario(cpf,nome,data_nascimento,endereco,usuarios)
    elif op == 5:
        num_conta = criar_conta(AGENCIA,num_conta, usuarios, contas)
    elif op == 6:
        mostrar_usuarios_e_contas(usuarios, contas)
    elif op == 0:
        break
    else:
        print("Opção inválida!")