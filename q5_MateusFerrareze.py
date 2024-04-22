from flask import Flask, request #aplicação servidor
import bcrypt #autenticidade senhas

#curl -X POST -d "login=user1&password=password1&transaction_type=cash&amount=100" http://127.0.0.1:5000/transaction
#copiar o comando acima no prompt de comando após executar,para realizar a aplicação de servidor com a autenticidade criptografada

app = Flask(__name__)

usuarios = [
    {
        'login': 'user1',
        'password_hash': bcrypt.hashpw('password1'.encode('utf-8'), bcrypt.gensalt()), #armazenamento e criptografia
        'current_amount': 2000.0,
        'agency': '011',
        'card_password': '1890' 
    },
    {
        'login': 'user2',
        'password_hash': bcrypt.hashpw('password2'.encode('utf-8'), bcrypt.gensalt()),
        'current_amount': 1500.0,
        'agency': '034',
        'card_password': '6745' 
    }
]

#autentificando 
def autenticar(login, password):
    user = next((user for user in usuarios if user['login'] == login), None)
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
        return user
    return None


detalhes_conta = lambda: request.form.get('card_password')
imprimir_recibo = lambda valor: f"Printing and returning receipt of R$ {valor:.2f}"
completar_transac = lambda: "Transaction Complete!"
fechar_transac = lambda: "Closing Transaction..."


def processar_dinheiro(user, valor):
    saldo_atual = user['current_amount']
    if saldo_atual < valor:
        return None, "Sorry...Transaction cancelled. Not enough funds."
    
    imprimir_recibo(valor)
    completar_transac()
    fechar_transac()
    
    novo_saldo = saldo_atual - valor
    return novo_saldo, None

def processar_transferencia(user, valor, agencia_destino):
    saldo_atual = user['current_amount']
    agencia_user = user['agency']
    
    if agencia_user != agencia_destino:
        return None, "Sorry...Transaction cancelled. Wrong agency number."
    
    novo_saldo = saldo_atual + valor
    return novo_saldo, "Payment approved from bank. Transaction closed."

def processar_credito(user, valor):
    saldo_atual = user['current_amount']
    
    senha_fornecida = detalhes_conta()
    
    if senha_fornecida != user['card_password']:
        return None, "Sorry..Transaction cancelled. Wrong card password."
    
    novo_saldo = saldo_atual - valor if saldo_atual >= valor else None
    
    if novo_saldo is not None:
        completar_transac()
        fechar_transac()
        return novo_saldo, "Payment approved from bank."
    else:
        return None, "Not enough funds."

def processar_pagamento(user, tipo_transacao, valor, agencia_destino=None):
    if tipo_transacao == 'cash':
        return processar_dinheiro(user, valor)
    elif tipo_transacao == 'fund transfer':
        return processar_transferencia(user, valor, agencia_destino)
    elif tipo_transacao == 'credit':
        return processar_credito(user, valor)

@app.route('/transaction', methods=['POST']) #método aplicação servidor
def transaction():
    login = request.form.get('login')
    password = request.form.get('password')

    user = autenticar(login, password)

    if user is None:
        return "Login or password invalid.", 401

    tipo_transacao = request.form.get('transaction_type')
    if tipo_transacao not in ['cash', 'fund transfer', 'credit']:
        return "Choice not available. Transaction closed.", 400
    
    valor = float(request.form.get('amount'))
    
    if tipo_transacao == 'fund transfer':
        agencia_destino = request.form.get('destination_agency')
    else:
        agencia_destino = None
    
    resultado_transacao, erro = processar_pagamento(user, tipo_transacao, valor, agencia_destino)

    if resultado_transacao is not None:
        user['current_amount'] = resultado_transacao
        return f"Transaction Successful. Your new amount: R$ {resultado_transacao:.2f}", 200
    else:
        return erro, 400

if __name__ == '__main__':
    app.run(debug=True)
