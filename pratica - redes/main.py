from user import User
from server import Server

server = Server()
cliente = User(server)

if __name__ == "__main__":

    while True:
        print('\n-------- Sistema de Cadastro TOTP2AUT --------'
              '\n---------- 1 - Cadastro de usuario -----------'
              '\n---------- 2 - Login -------------------------'
              '\n---------- 3 - Fechar ------------------------')
        escolha = input('\nDigite uma opção: ')
        if escolha == '1':
            cliente.create_user()
        elif escolha == '2':
            cliente.login()
        elif escolha == '3':
            break
        else:
            print('\nPor favor, insira um número inteiro entre 1 e 3 !!')
