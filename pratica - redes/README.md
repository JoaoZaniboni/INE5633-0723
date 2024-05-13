Tarefa Prática - INE5680-07238 (20241) - Segurança da Informação e de Redes
João Victor Neves Zaniboni (21100505) e Pedro Henrique Leão Schiavinatto (21104935)

O trabalho simula um sistema onde é possivel se cadastrar e fazer login utilizando autentificação de 2 fatores TOTP
Quando cadastrado, é possivel trocar mensagens com o sistema, sendo essas mensagens criptografadas autentificadas.

Para rodar o código, primeiro crie uma máquina virual e depois de o comando:
pip install -r 'requirements.txt'

Por fim, rode o arquivo main.py

quando se cadastrar, irá aparecer uma imagem qrcode, você deve ler essa mensagem qrcode com App de autentificação de 2 fatores, como o Authenticator do google.
Ao realizar login, irá pedir o código de 2 fatores, você deve pegar esse códgo no app que você cadastrou.