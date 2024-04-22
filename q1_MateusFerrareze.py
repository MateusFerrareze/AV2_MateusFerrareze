usuarios = [
    {
        'login': 'user1',
        'password': 'password1',
        'current amount': 2000.0,
        'agency': '011',
        'card password': '1890'  
    },
    {
        'login': 'user2',
        'password': 'password2',
        'current amount': 1500.0,
        'agency': '034',
        'card password': '6745'  
    }
]

autenticar = lambda login, password: next((user for user in usuarios if user['login'] == login and user['password'] == password), None)
detalhes_cartao = lambda: input("Please type your card password: ")
criar_transac = lambda: print("Creating Transaction...")
imprimir_recibo = lambda valor: print(f"Printing and returning receipt of R$ {valor:.2f}")
completar_transac = lambda: print("Transaction Complete!")
fechar_transac = lambda: print("Closing Transaction...")


def p_dinheiro(user, valor):
    saldo_atual = user['current amount']
    if saldo_atual < valor:
        print("Sorry...Transaction cancelled. Not enough funds.")
        return None
    
    imprimir_recibo(valor)
    completar_transac()
    fechar_transac()
    
    novo_saldo = saldo_atual - valor
    return novo_saldo


def p_transferencia(user, valor, agencia_destino):
    saldo_atual = user['current amount']
    agencia_user = user['agency']
    
    if agencia_user != agencia_destino:
        print("Sorry...Transaction cancelled. Wrong agency number.")
        return None
    
    novo_saldo = saldo_atual + valor
    if novo_saldo is not None:
        print("Payment approved from bank.")
        print("Transaction closed.")
    return novo_saldo


def p_credito(user, valor):
    saldo_atual = user['current amount']
    
    senha_fornecida = detalhes_cartao()
    
    if senha_fornecida != user['card password']:
        print("Sorry..Transaction cancelled. Wrong card password.")
        return None
    
    print("Requesting Payment from bank...")
    
    novo_saldo = saldo_atual - valor if saldo_atual >= valor else None
    
    if novo_saldo is not None:
        print("Payment approved from bank.")
        completar_transac()
        fechar_transac()
    
    return novo_saldo


def processar_pagamento(user, tipo_transacao, valor, agencia_destino=None):
    if tipo_transacao == 'cash':
        return p_dinheiro(user, valor)
    elif tipo_transacao == 'fund transfer':
        return p_transferencia(user, valor, agencia_destino)
    elif tipo_transacao == 'credit':
        return p_credito(user, valor)


def main():
    criar_transac()
    login = input("Please type your login/ID: ")
    password = input("Please type your password: ")

    user = autenticar(login, password)

    if user is None:
        print("Login or password invalid.")
        return

    tipo_transacao = input("Please choose an option (cash, fund transfer, credit): ")
    if tipo_transacao not in ['cash', 'fund transfer', 'credit']:
        print("Choice not available. Transaction closed.")
        return
    
    valor = float(input("How much will it be today: "))
    
    if tipo_transacao == 'fund transfer':
        agencia_destino = input("Please type your agency number: ")
    else:
        agencia_destino = None

    novo_saldo = processar_pagamento(user, tipo_transacao, valor, agencia_destino)

    if novo_saldo is None:
        print("Sorry...Transaction not possible.")
    else:
        user['current amount'] = novo_saldo
        print(f"Transaction Successful. Your new amount: R$ {novo_saldo:.2f}")

if __name__ == '__main__':
    main()
 