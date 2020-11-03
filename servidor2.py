import socket
from _thread import *
import time

nome = ''
dado = ''
data = ''

def escrita(s):
    global nome, dado, data
    nome = s.recv(1024).decode()
    dado = s.recv(1024).decode()
    data = s.recv(1024).decode()
    print('escrita')
    print('nome:', nome)
    print('dado:', dado)
    print('data:', data)

def leitura(s):
    global nome, dado, data
    s.send(str.encode(nome))
    time.sleep(1/100)
    s.send(str.encode(dado))
    time.sleep(1/100)
    s.send(str.encode(data))
    time.sleep(1/100)
    print('leitura')
    print('nome:', nome)
    print('dado:', dado)
    print('data:', data)

def leitura_escrita(s):
    opcao = s.recv(1024).decode()
    if opcao == 'escrita':
        escrita(s)
    elif opcao == 'leitura':
        leitura(s)
    else:
        print('comando não encontrado')

    s.close()

def main():
    s = socket.socket()
    host = '0.0.0.0'
    port = 5002

    try:
        s.bind((host, port))
    except socket.error as e:
        print(str(e))
    
    print('servidor 2 iniciado')

    s.listen(5)

    while True:
        client, address = s.accept()
        start_new_thread(leitura_escrita, (client, ))
    s.close()

main()