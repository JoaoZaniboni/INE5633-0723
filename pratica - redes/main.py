from user import User
from server import Server


def user_menu():
    while True:
        print('\n--------- Menu do usuario - TOTP2AUT ---------'
              '\n---- 1 - Enviar mensagem para sistema --------'
              '\n---- 2 - Desconectar -------------------------')
        escolha = input('\nDigite uma opção: ')
        if escolha == '1':
            pass
        elif escolha == '2':
            break

        else:
            print('\nPor favor, insira 1 ou 2 !!')

def main_menu(user):
    while True:
        print('\n-------- Sistema de Cadastro TOTP2AUT --------'
              '\n---------- 1 - Cadastro de usuario -----------'
              '\n---------- 2 - Login -------------------------'
              '\n---------- 3 - Fechar ------------------------')
        escolha = input('\nDigite uma opção: ')
        if escolha == '1':
            user.create_user()
        elif escolha == '2':
            if user.login():
                user_menu()
        elif escolha == '3':
            break
        else:
            print('\nPor favor, insira um número inteiro entre 1 e 3 !!')


if __name__ == "__main__":
    server = Server()
    user = User(server)
    main_menu(user)
