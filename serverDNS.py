import threading
import manager
import socket
HOST = manager.HOST
PORT = manager.PORT
DNSSERVERPORT=4041
ipServer = {}
portServer = {}


# ipServer = {"trabalho.com.br": '127.0.0.1'}
# portServer = {"trabalho.com.br": 4040}

def checkServerList(name):
    try:
        ipServer[name]
        return True
    except KeyError:
        return False


def checkServerStatus(serverIP, serverPort):
    print(serverIP)
    print(serverPort)
    statusOfServer = False
    try:
        socketWithServer = socket.socket(socket.AF_INET,
                                         socket.SOCK_STREAM)
        socketWithServer.connect((serverIP, int(serverPort)))
        manager.send_msg(socketWithServer, "Check\0")  # Blocks u
        statusOfServer = True
        print('\nServer {}:{} is online!'.format(serverIP, serverPort))
    except ConnectionError:
        print('\nServer {}:{} is offline'.format(serverIP, serverPort))
        statusOfServer = False
    finally:
        socketWithServer.close()
    return statusOfServer


def handle_client(sock, addr):

    try:
        msg = manager.recv_msg(sock)
        print(msg)
        if(msg[:3] == 'DNS'):
            print("APAGAR DSN REDUZIDO > "+ msg[:3] )
            msg = msg.split(':')
            ipServer[msg[3]] =msg[1]
            portServer[msg[3]] = msg[2]
            print(ipServer)
        else:
            if(checkServerList(msg)):
                if checkServerStatus(ipServer[msg], portServer[msg]):
                    adressOfserver = ipServer[msg] + ":" + str(portServer[msg])
                    print("Endereco a ser enviado: " + adressOfserver)
                    manager.send_msg(sock, adressOfserver)
                else:
                    manager.send_msg(sock, "Error 404!")
            else:
                manager.send_msg(sock, "Error 403!")
    except (ConnectionError, BrokenPipeError):
        print('Socket error')
    finally:
        print('Closed connection to {}'.format(addr))
        sock.close()


if __name__ == '__main__':
    listen_sock = manager.create_listen_socket('', DNSSERVERPORT)
    addr = listen_sock.getsockname()
    print('Listening on {}'.format(addr))
    while True:
        client_sock, addr = listen_sock.accept()
        # Thread will run function handle_client() autonomously
        # and concurrently to this while loop
        thread = threading.Thread(target=handle_client,
                                  args=[client_sock, addr],
                                  daemon=True)
        thread.start()
        print('Connection from {}'.format(addr))
