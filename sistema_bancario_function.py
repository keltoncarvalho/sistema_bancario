from datetime import datetime

def menu():
    '''Imprime o menu na tela e retorna a operação.'''
    print(f'''
{"MENU".center(35, '-')}
[ 1 ] Saque
[ 2 ] Deposito
[ 3 ] Extrato
[ 4 ] Novo Usuário
[ 5 ] Nova Conta
[ 6 ] Usuários Cadastrados
[ 7 ] Contas do Usuário
[ 0 ] Sair''')
    print()
    opcao = int(input('Operação: '))
    return opcao


def saque(*, saldo, valor, historico, limite, numero_saques, limite_saques):
    '''Função para realizar saque.'''
    if valor > saldo:
        print('Você não possui saldo suficiente.')
    elif valor > limite:
        print('Só é possível sacar até R$ 500.00')
    elif numero_saques >= limite_saques:
        print('Limite de saques atingido!')
    elif valor > 0:
        saldo -= valor
        data_e_hora = horario()
        historico += f'Saque:    R$ {valor:.2f}{data_e_hora.rjust(37-len(str(valor)))}\n'
        numero_saques += 1
    else: 
        print('Valor inválido.')
    return saldo, historico


def deposito(saldo, valor, historico, /):
    '''Função para depósito.'''
    saldo += valor
    data_e_hora = horario()
    historico += f'Depósito: R$ {valor:.2f}{data_e_hora.rjust(37-len(str(valor)))}\n'
    return saldo, historico


def extrato(saldo, /, *, historico):
    '''Função para exibir o extrato formatado.'''
    print(f'{"EXTRATO".center(55, '-')}')
    print()
    print(f'Nenhuma movimentação realizada.\n' if historico == '' else historico)
    print(f'Saldo:    R$ {saldo:>.2f}')
    return historico


def cpfs_cadastrados(clientes):
    '''Retorna uma lista com os CPFs já cadastrados.'''
    verifica_cpf = list()
    for pessoa in clientes:
        verifica_cpf.append(pessoa.get('CPF'))
    return verifica_cpf


def cadastro(clientes):
    '''Função para cadastro de clientes com verificação por CPF.'''
    cpf = str(input('Digite o CPF: ')).strip()
    lista_cpfs = cpfs_cadastrados(clientes)
    if cpf in lista_cpfs:
        print('Erro! Usuário já cadastrado.')
        return
    
    nome = str(input('Digite o Nome: ')).strip().title()
    nascimento = str(input('Digite a data de nascimento: ')).strip()
    endereco = str(input('Digite o endereco: ')).strip()
    clientes.append({'Nome': nome,'Data de Nascimento': nascimento,'CPF': cpf,'Endereço': endereco})
    print('Usuário cadastrado com sucesso!')
    

def criar_conta(clientes, agencia):
    '''Cria uma conta se o CPF informado estiver cadastrado.'''
    usuario = str(input('Digite o CPF do cliente: '))
    if usuario in cpfs_cadastrados(clientes):
        conta_criada = str(len(contas_do_banco) + 1)
        contas_do_banco.append({'Agência': agencia, 'Conta': conta_criada, 'Usuário': usuario})
        print('Conta criada com sucesso!')
    else:
        print('Erro! Usuário não cadastrado.')
    return


def contas_do_usuario(contas):
    '''Exibe as contas de um usuário de acordo com o CPF informado.'''
    cpf = str(input('CPF do usuário: '))
    for conta in contas:
        if conta.get('Usuário') == cpf:
            print(conta)
    return


def horario():
    '''Função para ler a data e hora do sistema.'''
    data_e_hora = datetime.strftime(datetime.now(), '%d/%m/%y %H:%M:%S')
    return data_e_hora


def mostrar_clientes(usuarios):
    '''Exibe os dados de cadastro dos clientes cadastrados em formato de dicionário.'''
    if len(usuarios) == 0:
        print('Nenhum usuário cadastrado.')
    else:
        for cliente in usuarios:
            print(cliente)
        return


def controle_de_transacao(historico, limite):
    dia_atual = datetime.now().day
    contagem = 0
    for transacao in historico.split(sep='\n'):
        string_date = transacao[30:].strip()
        if transacao != '':
            dia_da_transacao = datetime.strptime(string_date, '%d/%m/%y %H:%M:%S').day
            if dia_atual == dia_da_transacao:
                if contagem == limite:
                    break
                else:
                    contagem += 1
    return True if contagem == limite else False
    
AGENCIA = '0001'
LIMITE_TRANSACOES = 10
valor = 0
saldo = 0
saques = 0
historico = ''
usuarios = list()
contas_do_banco = list()

while True:
    operacao = menu()
    print()
    if operacao == 1:
        if controle_de_transacao(historico, LIMITE_TRANSACOES) == False:
            valor = float(input('Digite o valor: R$ '))
            print()
            saldo, historico = saque(saldo=saldo, valor=valor, historico=historico, numero_saques=saques, limite=500, limite_saques=3)
            print('Retire seu dinheiro.')
        else:
            print('Limite diário de transações atingido! Tente amanhã.')
            break
    elif operacao == 2:
        if controle_de_transacao(historico, LIMITE_TRANSACOES) == False:
            valor = float(input('Digite o valor: R$ '))
            saldo, historico = deposito(saldo, valor, historico)
            print('Depósito realizado com sucesso.')
        else:
            print('Limite diário de transações atingido! Tente amanhã.')
            break
    elif operacao == 3:
        extrato(saldo, historico=historico)
        break
    elif operacao == 4:
        cadastro(usuarios)
    elif operacao == 5:
        criar_conta(usuarios, AGENCIA)
    elif operacao == 6:
        mostrar_clientes(usuarios)
    elif operacao == 7:
        contas_do_usuario(contas_do_banco)
    elif operacao == 0:
        break
    else:
        print(f'Opção inválida! Tente novamente.'.center(35))
        continue
print('-'*55)
print(f'Obrigado por utilizar nossos serviço, volte sempre!'.center(55))
print('-'*55)
