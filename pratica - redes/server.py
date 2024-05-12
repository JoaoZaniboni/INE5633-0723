from Crypto.Protocol.KDF import scrypt
from pyotp.totp import TOTP
import qrcode
import base64


class Server:
    def __init__(self):
        self.__users = {}

    @property
    def users(self):
        return self.__users

    def apply_scrypt(self, key):
        salt = 'salt_hard_coded'
        scrypt_key = scrypt(key, salt, 16, N=2 ** 14, r=8, p=1)
        return scrypt_key

    def user_register(self, name, key):
        if name in self.users.keys():
            print('----- Usuário ja cadastrado no sistema!! -----')
            return False

        scrypt_key = self.apply_scrypt(key)
        self.users[name] = scrypt_key

        totp_auth = TOTP(base64.b32encode(scrypt_key)).provisioning_uri(name=name, issuer_name='UFSCJoao-Pedro')
        qrcode_image = qrcode.make(totp_auth)

        return qrcode_image

    def buscar_usuario(self, name, key):
        scrypt_key = self.apply_scrypt(key)

        if name in self.users.keys():
            if self.users[name] == scrypt_key:
                auth_2fa = self.apply_2factor(scrypt_key)

                if auth_2fa:
                    return True

        return False

    def apply_2factor(self, scrypt_key):
        while True:
            totp = TOTP(base64.b32encode(scrypt_key))
            totp_input = input('Digite o código de autenticação de 2 fatores do App: ')

            if totp.verify(totp_input):
                print("\nCódigo de autenticação de 2 fatores validado")
                return True
            print("\nCódigo de autenticação de 2 fatores invalido, tente novamente!!")