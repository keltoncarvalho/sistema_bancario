from datetime import datetime
from abc import ABC, abstractmethod
import textwrap


class Cliente:
    def __init__(self, endereco=str):
        self.endereco = endereco
        self.contas = list()

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
    

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0.00
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod #permite a execução da função diretemente sem instanciar um objeto
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)#retorna uma instancia de Conta
    
    @property #permite acesso da função como uma propriedade
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
        saldo = self.saldo

        if valor > saldo:
            print('Você não possui saldo suficiente.')
        elif valor > 0:
            self._saldo -= valor
            print('Saque realizado com sucesso.')
            return True
        else: 
            print('Falha ao executar operação. O valor informado é inválido.')
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print('Depósito realizado com sucesso.')
            return True
        else:
            print('Falha ao executar operação. O valor informado é inválido.')
        return False
        

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, 
                 limite_operacao_saque=500.00, 
                 limite_de_saques=3):
        super().__init__(numero, cliente)
        self.limite_operacao_saque = limite_operacao_saque
        self.limite_de_saques = limite_de_saques

    def sacar(self, valor):
        saques_realizados = len([transacao for transacao in 
                                 self.historico.transacoes if 
                                 transacao['tipo'] == Saque.__name__])
        
        if valor > self.limite_operacao_saque:
            print('Não é possível sacar mais de R$500.00')
        elif saques_realizados >= self.limite_de_saques:
            print('Limite de saques diários excedido. Tente amanhã.')
        else:
            return super().sacar(valor)
        return False
    
    def __str__(self): #metodo de representacao da classe
        return f'''\
                Agência:\t{self.agencia}
                C/C:\t\t{self.numero}
                Titular:\t{self.cliente.nome}
                '''
    

class Historico:
    def __init__(self):
        self._transacoes = list()

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({'tipo': transacao.__class__.__name__,
                                 'valor': transacao.valor,
                                 'data': datetime.now().strftime(
                                     '%d/%m/%Y %H:%M:%s')
                                 })


class Transacao(ABC): #enquanto abstract valores 'pass' serão definidos nas classes filhas
    @property
    @abstractmethod #obriga as classes filhas a implementar esse método
    def valor(self):
        pass

    @classmethod
    @abstractmethod 
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor : float):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor) == True:
            conta.historico.adicionar_transacao(self)

        
class Deposito(Transacao):
    def __init__(self, valor : float):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor) == True:
            conta.historico.adicionar_transacao(self)
        

def menu():
    '''Imprime o menu na tela e retorna a operação.'''
    print(f'''
{"MENU".center(55, '=')}
[ 1 ] Saque
[ 2 ] Deposito
[ 3 ] Extrato
[ 4 ] Cadastrar Cliente
[ 5 ] Criar Conta
[ 6 ] Listar Contas
[ 0 ] Sair''')
    print()
    opcao = int(input('Operação: '))
    return opcao

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in 
                          clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print('Cliente não possui conta!')
        return
    
    return cliente.contas[0] #Assume que o cliente só tem uma conta


def sacar(clientes):
    '''Função para realizar saque.'''
    cpf = input('CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não encontrado!')
        return
    
    valor = float(input('Informe o valor do saque: '))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)


def depositar(clientes):
    '''Função para depósito.'''
    cpf = input('CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não encontrado!')
        return
    
    valor = float(input('Informe o valor do depósito: '))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    '''Função para exibir o extrato formatado.'''
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não encontrado!')
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print(f'{"EXTRATO".center(55, '=')}')
    print()
    transacoes = conta.historico.transacoes

    extrato = ''
    if not transacoes:
        extrato = 'Nenhuma movimentação realizada.'
    else:
        for transacao in transacoes:
            extrato += f"{transacao['tipo']}:  \tR$ {transacao['valor']:>8.2f}\n"

    print(extrato)
    print(f'\nSaldo:\t\tR$ {conta.saldo:.2f}\n')
    print('='*55)


def cadastrar_cliente(clientes):
    '''Função para cadastro de clientes com verificação por CPF.'''
    cpf = input('Digite o CPF: ')
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print('Erro! Cliente já cadastrado.')
        return
    
    nome = input('Digite o Nome: ').strip()
    data_nascimento = input('Digite a data de nascimento (dd-mm-aaaa): ').strip()
    endereco = input('Digite o endereco (logradouro, nro - bairro - cidade/sigla estado): ').strip()
    
    cliente = PessoaFisica(nome=nome,
                           data_nascimento=data_nascimento,
                           cpf=cpf, endereco=endereco)
    
    clientes.append(cliente)
    print('Cliente cadastrado com sucesso!')
    

def criar_conta(numero_conta, clientes, contas):
    '''Cria uma conta se o CPF informado estiver cadastrado.'''
    cpf = input('Digite o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não encontrado. Criação de conta interrompida.')
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, 
                                     numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print('\nConta criada com sucesso!')


def listar_contas(contas):
    for conta in contas:
        print('=' * 55)
        print(textwrap.dedent(str(conta)))
    
    
def main():
    clientes = list()
    contas = list()

    while True:
        operacao = menu()
        print()
        if operacao == 1:
            sacar(clientes)
        elif operacao == 2:
            depositar(clientes)
        elif operacao == 3:
            exibir_extrato(clientes)
        elif operacao == 4:
            cadastrar_cliente(clientes)
        elif operacao == 5:
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif operacao == 6:
            listar_contas(contas)
        elif operacao == 0:
            break
        else:
            print(f'Opção inválida! Tente novamente.'.center(35))
            continue
    print('='*55)
    print(f'Obrigado por utilizar nossos serviço, volte sempre!'.center(55))
    print('='*55)

main()
