import socket
from _thread import *
import datetime
import time

servidorNumero = 1
opcaoEscrita, novosDados = 1, False

def atualizar():
    global novosDados
    while True:
        time.sleep(5)
        if novosDados == True:
            if opcaoEscrita == 1:
                s = conectar_servidor(5001)
            elif opcaoEscrita == 2:
                s = conectar_servidor(5002)
            nome, dado, data = enviarServidor(s, 'leitura', '', '', '')
            print('Atualizacao dos dados realizadas')
            if opcaoEscrita == 1:
                s = conectar_servidor(5002)
                print('servidor: 2')
            elif opcaoEscrita == 2:
                s = conectar_servidor(5001)
                print('servidor: 1')
            enviarServidor(s, 'escrita', nome, dado, data)
            s.close()
            print('nome:', nome)
            print('dado:', dado)
            print('data:', data)
            novosDados = False

def conectar_servidor(port):
    s = socket.socket()
    host = '127.0.0.1'

    try:
        s.connect((host, port))
    except socket.error as e:
        print(str(e))
    return s

def enviarServidor(s, opcao, nome, dado, data):
    if opcao == 'escrita':
        s.send(str.encode(opcao))
        time.sleep(1/100)
        s.send(str.encode(nome))
        time.sleep(1/100)
        s.send(str.encode(dado))
        time.sleep(1/100)
        s.send(str.encode(data))
        time.sleep(1/100)
    elif opcao == 'leitura':
        s.send(str.encode(opcao))
        nome = s.recv(1024).decode()
        dado = s.recv(1024).decode()
        data = s.recv(1024).decode()
    return nome, dado, data

def servidor(opcao, nome, dado, data):
    global servidorNumero, opcaoEscrita, novosDados
    print('nova requisicao')
    print('requisicao de:', opcao)
    print('enviada para o servidor:', servidorNumero)
    if opcao == 'escrita':
        opcaoEscrita = servidorNumero
        novosDados = True
    if servidorNumero == 1:
        s = conectar_servidor(5001)
        nome, dado, data = enviarServidor(s, opcao, nome, dado, data)
        s.close()
        servidorNumero = 2
    elif servidorNumero == 2:
        s = conectar_servidor(5002)
        nome, dado, data = enviarServidor(s, opcao, nome, dado, data)
        s.close()
        servidorNumero = 1
    else:
        print('erro, requisicao nao enviada')
    print('nome:', nome)
    print('dado:', dado)
    print('data:', data)
    return nome, dado, data

def leitura(s):
    nome, dado, data = servidor('leitura', '', '', '')
    s.send(str.encode(nome))
    time.sleep(1/100)
    s.send(str.encode(dado))
    time.sleep(1/100)
    s.send(str.encode(data))
    time.sleep(1/100)

def escrita(s):
    nome = s.recv(1024).decode()
    dado = s.recv(1024).decode()
    data = str(datetime.datetime.now())
    servidor('escrita', nome, dado, data)

def leitura_escrita(s):
    opcao = ''
    while opcao != 'sair':
        opcao = s.recv(1024).decode()
        if opcao == 'escrita':
            escrita(s)
        elif opcao == 'leitura':
            leitura(s)
        else:
            if opcao != 'sair':
                print('erro')

def main():
    s = socket.socket()
    host = '0.0.0.0'
    port = 5000

    try:
        s.bind((host, port))
    except socket.error as e:
        print(str(e))
    
    print('diretorio ativo')

    start_new_thread(atualizar, ())

    s.listen(5)

    while True:
        client, address = s.accept()
        start_new_thread(leitura_escrita, (client, ))
    s.close()

main()