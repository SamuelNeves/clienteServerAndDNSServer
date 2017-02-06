import threading
import manager
import socket
HOST = '127.0.0.1'
PORT = 4040
DNSSERVERIP = '127.0.0.1'
DNSSERVERPORT = 4041
name='trabalho.com.br'
def startDNS():
    try:
        print("trying to send name!")
        socketWithDNS = socket.socket(socket.AF_INET,
                                         socket.SOCK_STREAM)
        socketWithDNS.connect((DNSSERVERIP, DNSSERVERPORT))
        data="DNS:"+HOST+":"+str(PORT)+":"+name
        print(data)
        manager.send_msg(socketWithDNS, data)
    except ConnectionError:
        print('Socket error')
    finally:
        print('Closed connection ')
        socketWithDNS.close()


def handle_client(sock, addr):
    """ Receive one message and echo it back to client, then close
    socket """
    try:
        msg = manager.recv_msg(sock)

        if(msg == 'Check'):
            print('dsadsadsadsa')
        else:

            # blocks until received
            # complete message
            # msg = '{}: {}'.format(addr, msg)
            # msg = "FUI CHECADO\0"
            print(msg)
            manager.send_msg(sock, msg)  # blocks until sent
    except (ConnectionError, BrokenPipeError):
        print('Socket error')
    finally:
        print('Closed connection to {}'.format(addr))
        sock.close()


if __name__ == '__main__':
    startDNS()
    listen_sock = manager.create_listen_socket(HOST, PORT)
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
