import sys
import socket
import manager
HOST = sys.argv[-1] if len(sys.argv) > 1 else '127.0.0.1'
PORT = 4041


def checkAdress(name):
    try:
        sock = socket.socket(socket.AF_INET,
                             socket.SOCK_STREAM)
        sock.connect((HOST, 4041))
        manager.send_msg(sock, name)

        msg = manager.recv_msg(sock)  # Block until
        # received complete
        # message
        try:
            [serverIP, serverPort] = msg.split(':')
        except ValueError:
            [serverIP, serverPort] = [False, msg]
    except ConnectionError:
        print('Socket error')
    finally:
        sock.close()
        print('Closed connection to DNS server\n')
    return [serverIP, serverPort]


def doSomethingInServer(serverIP, serverPort):
    try:
        sock = socket.socket(socket.AF_INET,
                             socket.SOCK_STREAM)
        sock.connect((serverIP, int(serverPort)))
        print("Insert the data to send")
        msg = input()
        manager.send_msg(sock, msg)

        msg = manager.recv_msg(sock)  # Block until
        # received complete
        # message
        # [serverIP, serverPort] = msg.split(':')
        print('Received echo: ' + msg)
    except ConnectionError:
        print('Socket error')
    finally:
        sock.close()
        print('Closed connection to server\n')


if __name__ == '__main__':
    print("Please insert the website:")
    name = input()
    [serverIP, serverPORT] = checkAdress(name)
    if(serverIP):
        while(True):
            doSomethingInServer(serverIP, serverPORT)
    else:
        print(serverPORT)
