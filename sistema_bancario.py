import datetime

valor = 0
saldo = 0
LIMITE_SAQUES = 3
LIMITE_TRANSACOES = 10
transacoes = 0
saques = 0
opcao = -1
extrato = ''
data_e_hora = ''

while True:
    print(f'''
{"MENU".center(35, '-')}
[ 1 ] Saque
[ 2 ] Deposito
[ 3 ] Extrato
[ 0 ] Sair''')
    print()
    opcao = int(input('Operação: '))
    print()
    if opcao not in range(0, 4):
        print(f'Opção inválida! Tente novamente.'.center(35))
        continue
    elif opcao == 0:
        break
    elif opcao == 3:
        print('-'*54)
        print(f'{"EXTRATO".center(55)}')
        print()
        print(f'Nenhuma movimentação realizada.\n' if extrato == '' else extrato)
        print(f'Saldo: R$ {saldo:.2f}')
        break
    else:
        if transacoes == LIMITE_TRANSACOES:
            print('Não foi possível realizar a operação.\nLimite de transações diário atigido.\nTente novamente amannhã.')
        else:
            valor = float(input('Digite o valor: R$ '))
            print('-'*35)
            if valor < 0:
                print('VALOR INVÁLIDO!')
                continue
            if opcao == 1:
                if valor > saldo:
                    print('Você não possui saldo suficiente.')
                    continue
                else:
                    if saques >= LIMITE_SAQUES:
                        print('Limite de saques atingido!')
                    elif valor > 500:
                        print('Só é possível sacar até R$ 500.00')
                    else:
                        saldo -= valor
                        data_e_hora = datetime.datetime.strftime(datetime.datetime.now(), '%d/%m/%y %H:%M:%S')
                        saques += 1
                        transacoes += 1
                        extrato += f'Saque: R$ {valor:.2f}{data_e_hora.rjust(40-len(str(valor)))}\n'
                        print('Retire o seu dinheiro.')
            elif opcao == 2:
                saldo += valor
                data_e_hora = datetime.datetime.strftime(datetime.datetime.now(), '%d/%m/%y %H:%M:%S')
                transacoes += 1
                extrato += f'Depósito: R$ {valor:.2f}{data_e_hora.rjust(37-len(str(valor)))}\n'
                print('Depósito realizado com sucesso.')
print('-'*55)
print(f'Obrigado por utilizar nossos serviço, volte sempre!'.center(55))
print('-'*55)
