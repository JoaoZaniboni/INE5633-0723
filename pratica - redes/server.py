# Importação das bibliotecas necessárias
from Crypto.Protocol.KDF import scrypt
from pyotp.totp import TOTP
import qrcode
import base64
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Cipher import AES

# Definição da classe Server
class Server:
    # Método de inicialização da classe
    def __init__(self):
        # Dicionário para armazenar os usuários e suas chaves
        self.__users = {}
        # Chave de sessão, inicializada como None
        self.__session_key = None

    # Getter para a chave de sessão
    @property
    def session_key(self):
        return self.__session_key

    # Setter para a chave de sessão
    @session_key.setter
    def session_key(self, key):
        self.__session_key = key

    # Getter para os usuários
    @property
    def users(self):
        return self.__users

    # Método para aplicar o algoritmo scrypt
    def apply_scrypt(self, namekey, salt):
        # Embaralha o salt utilizando uma cifra de César simples
        salt = self.ceaser_cypher(salt, len(salt))
        # Aplica o algoritmo scrypt para criar uma chave
            # namekey = user + senha
            # salt = cifra de cesar no username usando tamanho como chave
            # 32 =  comprimento da chave de saida (bytes)
            # N = custo de memoria
            # r = tamanho sequencia
            # p = paralelismo
        scrypt_key = scrypt(namekey, salt, 32, N=16384, r=8, p=1)
        return scrypt_key

    # Método para registrar um novo usuário no sistema
    def user_register(self, name, key):
        # Verifica se o usuário já está cadastrado
        if name in self.users.keys():
            print('\n----- Usuário já cadastrado no sistema!! -----')
            return False

        # Aplica o algoritmo scrypt para gerar a chave do usuário
        scrypt_key = self.apply_scrypt(name.encode()+key, name)
        # Armazena o usuário e sua chave no dicionário de usuários
        self.users[name] = scrypt_key
        # Gera um código TOTP para o usuário ()
        totp = TOTP(base64.b32encode(scrypt_key)).provisioning_uri(name=name, issuer_name='UFSCJoao-Pedro')
        # Gera um QR code com o código TOTP
        qrcode_image = qrcode.make(totp)

        return qrcode_image

    # Método para verificar se um usuário existe e a chave fornecida corresponde à chave registrada
    def seek_user(self, name, key):
        # Aplica o algoritmo scrypt para gerar a chave do usuário
        scrypt_key = self.apply_scrypt(name.encode()+key, name)

        # Verifica se o usuário está no dicionário de usuários e se a chave fornecida corresponde à chave registrada
        if name in self.users.keys():
            if self.users[name] == scrypt_key:
                return True
        return False

    # Método para criar uma chave a partir de uma senha e um salt utilizando o algoritmo PBKDF2
    def create_key(self, pwd, salt):
        # Embaralha o salt utilizando uma cifra de César simples
        salt = self.ceaser_cypher(salt, len(salt))
        # Aplica o algoritmo PBKDF2 para criar a chave
        key = PBKDF2(pwd, salt, count=1000, hmac_hash_module=SHA256)
        return key

    # Método para aplicar o segundo fator de autenticação utilizando um código TOTP
    def apply_2factor(self, name, key, totp_input):
        # Aplica o algoritmo scrypt para gerar a chave do usuário
        scrypt_key = self.apply_scrypt(name.encode()+key, name)
        # Cria um objeto TOTP com a chave do usuário
        totp = TOTP(base64.b32encode(scrypt_key))
        # Verifica se o código TOTP fornecido pelo usuário está correto
        if totp.verify(totp_input):
            # Cria uma chave de sessão
            self.session_key = self.create_key(totp_input, name)
            return True
        return False

    # Método para criptografar uma mensagem utilizando AES-GCM
    def autenticated_encrypt(self, msg, session_key):
        # Converte a mensagem para bytes
        msg = msg.encode()

        # Cria um objeto AES com o modo de operação GCM
        cipher = AES.new(session_key, AES.MODE_GCM)
        # Criptografa a mensagem e calcula o código de autenticação (MAC)
        encrypted_msg, mac = cipher.encrypt_and_digest(msg)

        return cipher.nonce + mac + encrypted_msg

    # Método para descriptografar uma mensagem e verificar sua autenticidade
    def autenticated_decrypt(self, concatenated_msg, session_key):
        # Divide a mensagem concatenada em nonce, MAC e mensagem criptografada
        nonce = concatenated_msg[:16]
        mac = concatenated_msg[16:32]
        encrypted_msg = concatenated_msg[32:]

        # Cria um objeto AES com o modo de operação GCM e o nonce fornecido
        cipher = AES.new(session_key, AES.MODE_GCM, nonce=nonce)
        try:
            # Descriptografa a mensagem e verifica o MAC
            decrypted_msg = cipher.decrypt_and_verify(encrypted_msg, mac)
        except ValueError:
            # Em caso de erro, a mensagem foi modificada
            print("Cuidado, a mensagem foi modificada!!")
            return False

        # Converte a mensagem descriptografada para string, se necessário
        if isinstance(decrypted_msg, bytes):
            decrypted_msg = decrypted_msg.decode()

        return decrypted_msg

    # Método para receber uma mensagem criptografada, descriptografá-la e enviar uma resposta criptografada
    def receive_than_send_msg(self, msg):
        # Descriptografa a mensagem recebida
        decrypted_msg = self.autenticated_decrypt(msg, self.session_key)
        if decrypted_msg:
            # Cria uma resposta à mensagem recebida
            msg_to_send = f"Lido mensagem '{decrypted_msg}', mas usuário, eu sou uma máquina sem IA, por enquanto ainda não consigo gerar respostas legais..."
            # Criptografa a resposta e a envia
            return self.autenticated_encrypt(msg_to_send, self.session_key)
        return False

    # Método para aplicar a cifra de César
    def ceaser_cypher(self, text, key):
        encrypted = ""
        for char in text:
            # Verifica se o caractere é uma letra
            if char.isalpha():
                # Aplica a cifra de César para embaralhar o caractere
                encrypted += chr((ord(char) + key - 97) % 26 + 97)
            else:
                # Mantém caracteres não alfabéticos inalterados
                encrypted += char
        return encrypted
