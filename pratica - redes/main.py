from user import User
from server import Server

cliente = User()

if __name__ == "__main__":

    while True:
        print('\nO que deseja fazer? \n1 - Cadastro \n2 - Login \n3 - Sair')
        escolha = input()
        if escolha == '1':
            cliente.create_user()
        elif escolha == '2':
            cliente.login()
        elif escolha == '3':
            break
        else:
            print('Por favor, insira um número inteiro entre 1 e 3')
