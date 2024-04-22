import threading
from q1_MateusFerrareze import usuarios, processar_pagamento

#teste de stress com 10 threads
for i in range(10):
    t = threading.Thread(target=lambda: [processar_pagamento(usuarios[i % len(usuarios)], 'cash', 500) for _ in range(1000)])
    t.start()

for t in threading.enumerate():
    if t != threading.current_thread():
        t.join()
print("Teste de stress concluído com suceso!")

#teste unitário transação ok
user = usuarios[0]
assert processar_pagamento(user, 'cash', 1000) == 1000.0
print("Teste com saldo suficiente concluído com sucesso!")

#teste unitário transação cancelada
assert processar_pagamento(user, 'cash', 3000) is None
print("Teste com saldo insuficiente concluído com sucesso!")

#teste unitário conta errada
assert processar_pagamento(user, 'fund transfer', 500, '002') is None
print("Teste com agência incorreta concluído com sucesso!")














