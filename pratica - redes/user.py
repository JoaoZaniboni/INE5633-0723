from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Cipher import AES

class User:
    def __init__(self, server):
        # Inicialização do objeto User
        self.server = server
        self.__session_key = None

    # Getter para a chave de sessão
    @property
    def session_key(self):
        return self.__session_key

    # Setter para a chave de sessão
    @session_key.setter
    def session_key(self, key):
        self.__session_key = key

    # Método para criar uma chave a partir de uma senha e um salt utilizando o algoritmo PBKDF2
    def create_key(self, pwd, salt):
        salt = self.ceaser_cypher(salt, len(salt))
        key = PBKDF2(pwd, salt, count=1000, hmac_hash_module=SHA256)
        return key

    # Método para criar um novo usuário
    def create_user(self):
        # Solicita o nome de usuário e a senha ao usuário
        name = input('Nome de usuário: ')
        pwd = input('Senha: ')
        
        # Verifica se o nome de usuário e a senha não estão vazios
        if not name or not pwd:
            print('\n----- Senha e Nome de usuário não podem estar vazios!! -----')
            return
        
        # Cria uma chave a partir da senha e do nome de usuário
        key = self.create_key(pwd, name)
        
        # Chama o método de registro de usuário do servidor, passando o nome de usuário e a chave
        qrcode_image = self.server.user_register(name, key)
        qrcode_image.show()

        print('\n----- Usuário cadastrado!! -----')

    # Método para realizar o login do usuário
    def login(self):
        # Solicita o nome de usuário e a senha ao usuário
        name = input('Nome de usuário: ')
        pwd = input('Senha: ')

        # Cria uma chave a partir da senha e do nome de usuário
        key = self.create_key(pwd, name)

        # Verifica se o usuário e a senha são válidos
        if not self.server.seek_user(name, key):
            print('\n----- Usuário e/ou senha inválidos!! -----')
            return False

        # Tentativas para o segundo fator de autenticação
        trys = 0
        while trys <= 2:
            totp_input = input('\nDigite o código de autenticação de 2 fatores do App: ')
            if self.server.apply_2factor(name, key, totp_input):
                print('\n------ Login realizado com sucesso  ------'
                      '\n--------------- Bem Vindo ---------------')
                # Cria uma chave de sessão
                self.session_key = self.create_key(totp_input, name)
                return True
            trys += 1
            print(f"\nCódigo de autenticação de 2 fatores inválido! Tentativas restantes: {trys}/3")

        print('\n-- Tentativas excedidas do segundo fator --')
        return False

    # Método para criptografar uma mensagem utilizando AES-GCM
    def autenticated_encrypt(self, msg, session_key):
        msg = msg.encode()

        cipher = AES.new(session_key, AES.MODE_GCM)
        encrypted_msg, mac = cipher.encrypt_and_digest(msg)

        return cipher.nonce + mac + encrypted_msg

    # Método para descriptografar uma mensagem e verificar sua autenticidade
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

    # Método para enviar uma mensagem criptografada e receber uma resposta criptografada do servidor
    def send_than_receive_msg(self, msg):
        # Criptografa a mensagem utilizando a chave de sessão
        encrypted_msg = self.autenticated_encrypt(msg, self.session_key)
        # Envia a mensagem criptografada para o servidor e recebe uma resposta criptografada
        response_msg = self.server.receive_than_send_msg(encrypted_msg)
        if response_msg:
            # Descriptografa a resposta recebida do servidor
            decrypted_msg = self.autenticated_decrypt(response_msg, self.session_key)
            print(decrypted_msg)

    # Método para aplicar a cifra de César
    def ceaser_cypher(self, text, key):
        encrypted = ""
        for char in text:
            if char.isalpha():
                encrypted += chr((ord(char) + key - 97) % 26 + 97)
            else:
                encrypted += char
        return encrypted
