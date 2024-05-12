from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from server import Server

class User:
    def __init__(self):
        self.server = Server()

    def create_key(self, pwd):
        salt = 'salt_hard_coded_again'
        key = PBKDF2(pwd, salt, count=1000, hmac_hash_module=SHA512)
        return key

    def create_user(self):
        name = input('Nome de usuário: ')
        pwd = input('Senha: ')

        key = self.create_key(pwd)
        qrcode_image = self.server.user_register(name, key)
        qrcode_image.show()

        print('\n----- Usuário cadastrado!! -----')

    def login(self):
        name = input('Nome de usuário: ')
        pwd = input('Senha: ')

        key = self.create_key(pwd)

        if not self.server.buscar_usuario(name, key):
            print('\n----- Usuário e/ou senha inválidos!! -----')
            return

        if self.server.apply_2factor(key):
            print('\n------ Login realizado com sucesso  ------'
                  '\n--------------- Bem Vindo ---------------')
        else:
            print('\n-- Tentativas excedidas do segundo fator --')
