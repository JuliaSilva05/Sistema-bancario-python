menu = """
[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair
=> """

saldo = 0
limite = 500
extrato = ""
n_saques = 0
LIMITE_SAQUES = 3


while True:
    op = int(input(menu))
    if op == 1:
        valor = float(input("Informe o valor do depósito: "))
        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
        else:
            print("Informe um valor válido")
    elif op == 2:
        valor = float(input("Informe o valor do saque: "))
        if n_saques == LIMITE_SAQUES:
            print("Limite de saques atingido!")   
            continue                 
        if valor > limite:
            print("O valor deve ser menor que R$ 500.00")
            continue
        if valor > 0 and saldo >= valor:
            n_saques += 1
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
        else:
            print("Valor inválido!")
    elif op == 3:
        print("EXTRATO")
        if extrato == "":
            print("Não foram realizadas movimentações")
        else:
            print(extrato)
            print(f"Saldo: R$ {saldo:.2f}")
    elif op == 0:
        break
    else:
        print("Opção inválida!")
