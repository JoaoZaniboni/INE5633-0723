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
        name = input('Digite seu nome de usuário:')
        pwd = input('Digite sua senha:')

        key = self.create_key(pwd)
        qrcode_auth = self.server.user_register(name, key)

        if qrcode_auth is False:
            return

        qrcode_auth.show()

        print('Usuário cadastrado!!')

    def login(self):
        name = input('Digite seu nome de usuário:')
        pwd = input('Digite sua senha:')

        key = self.create_key(pwd)
        user = self.server.buscar_usuario(name, key)

        if user is False:
            print('Usuário e/ou senha inválidos!!')
            return

        print('Login realizado com sucesso!!')
