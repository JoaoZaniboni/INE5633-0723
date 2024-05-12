from Crypto.Protocol.KDF import scrypt
from pyotp.totp import TOTP
import qrcode
import base64
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Cipher import AES

class Server:
    def __init__(self):
        #dicionario usuario - chave
        self.__users = {}
        self.__session_key = None

    @property
    def session_key(self):
        return self.__session_key

    @session_key.setter
    def session_key(self, key):
        self.__session_key = key

    @property
    def users(self):
        return self.__users

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

    def seek_user(self, name, key):
        scrypt_key = self.apply_scrypt(key)

        if name in self.users.keys():
            if self.users[name] == scrypt_key:
                return True
        return False

    def create_key(self, pwd):
        salt = 'salt_hard_coded_again'
        key = PBKDF2(pwd, salt, count=1000, hmac_hash_module=SHA256)
        return key

    def apply_2factor(self, key, totp_input):
        scrypt_key = self.apply_scrypt(key)
        totp = TOTP(base64.b32encode(scrypt_key))
        if totp.verify(totp_input):
            self.session_key = self.create_key(totp_input)
            return True
        return False

    def autenticated_encrypt(self, msg, session_key):
        msg = msg.encode()

        cipher = AES.new(session_key, AES.MODE_GCM)
        encrypted_msg, mac = cipher.encrypt_and_digest(msg)

        return cipher.nonce + mac + encrypted_msg

    def autenticated_decrypt(self, concatenated_msg, session_key):
        nonce = concatenated_msg[:16]
        mac = concatenated_msg[16:32]
        encrypted_msg = concatenated_msg[32:]

        cipher = AES.new(session_key, AES.MODE_GCM, nonce=nonce)
        try:
            decrypted_msg = cipher.decrypt_and_verify(encrypted_msg, mac)
        except ValueError:
            print("Cuidado, a mensagem foi modificada!!")
            return False

        if isinstance(decrypted_msg, bytes):
            decrypted_msg = decrypted_msg.decode()

        return decrypted_msg


    def receive_than_send_msg(self, msg):
        decrypted_msg = self.autenticated_decrypt(msg, self.session_key)
        if decrypted_msg:
            msg_to_send = f"Lido mensagem '{decrypted_msg}', mas usuário, eu sou uma máquina sem IA, por enquanto ainda não consigo gerar respostas legais..."
            return self.autenticated_encrypt(msg_to_send, self.session_key)
        return False
