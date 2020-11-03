import socket

def main():
    s = socket.socket()
    host = '127.0.0.1'
    port = 5000

    try:
        s.connect((host, port))
    except socket.error as e:
        print(str(e))

    print('1 - Atualizar dado')
    print('2 - Ler dado')
    print('3 - Sair')

    opcao = ''

    while opcao != 3:   

        opcao = int(input('Opcao: '))

        if opcao == 1:
            s.send(str.encode('escrita'))

            nome = input('Digite seu nome: ')
            s.send(nome.encode())

            dado = input('Digite o novo dado: ')
            s.send(dado.encode())

            print('requisicao enviada')

        elif opcao == 2:
            s.send(str.encode('leitura'))

            nome = s.recv(1024).decode()
            print('nome: ', nome)

            dado = s.recv(1024).decode()
            print('dado: ', dado)

            data = s.recv(1024).decode()
            print('data: ', data)
        
        else:
            if opcao != 3:
                print('opcao invalida')
            else:
                s.send(str.encode('sair'))

    s.close()

main()