from Crypto.Protocol.KDF import scrypt
from pyotp.totp import TOTP
import qrcode
import base64


class Server:
    def __init__(self):
        #dicionario usuario - chave
        self.users = {}

    def apply_scrypt(self, key):
        salt = 'salt_hard_coded'
        scrypt_key = scrypt(key, salt, 32, N=16384, r=8, p=1)
        return scrypt_key

    def user_register(self, name, key):
        if name in self.users.keys():
            print('\n----- Usuário ja cadastrado no sistema!! -----')
            return False

        scrypt_key = self.apply_scrypt(key)
        self.users[name] = scrypt_key
        totp = TOTP(base64.b32encode(scrypt_key)).provisioning_uri(name=name, issuer_name='UFSCJoao-Pedro')
        qrcode_image = qrcode.make(totp)

        return qrcode_image

    def buscar_usuario(self, name, key):
        scrypt_key = self.apply_scrypt(key)

        if name in self.users.keys():
            if self.users[name] == scrypt_key:
                return True
        return False

    def apply_2factor(self, key):
        scrypt_key = self.apply_scrypt(key)
        trys = 0
        while trys <= 2:
            totp = TOTP(base64.b32encode(scrypt_key))
            totp_input = input('\nDigite o código de autenticação de 2 fatores do App: ')

            if totp.verify(totp_input):
                print("\nCódigo de autenticação de 2 fatores validado!")
                return True
            trys += 1
            print(f"\nCódigo de autenticação de 2 fatores invalido! Chances: {trys}/3")