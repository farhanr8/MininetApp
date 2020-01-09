from socket import *
import threading
import time


def server_listener(s):
    print '----- Rendering Started -----'
    while 1:
        text = s.recv(1024)
        if text == 'TEARDOWN':
            s.send('OK')
            break
        print text
        time.sleep(1)
        s.send('OK')


# Create sockets for controller to connect to
PORT = 2002

try:
    s1 = socket(AF_INET, SOCK_STREAM)
except error as err:
    print 'Controller socket creation failed with error %s' % err
s1.bind(('', PORT))
s1.listen(1)

while 1:
    print '\nRenderer Listening...'
    conn, addr = s1.accept()
    print '\nConnected by', addr

    try:
        request = conn.recv(1024)
        cmd = request.split()[0]
        if cmd == 'SETUP':
            fileNum = request.split()[1]

            # Renderer connecting to Server
            server_port = 2001
            #server_ip = '192.168.1.88'
            server_ip = '10.0.0.1'
            try:
                s2 = socket(AF_INET, SOCK_STREAM)
            except error as err:
                print 'Server socket creation failed with error %s' % err
            s2.connect((server_ip, server_port))
            s2.send(request)
            if s2.recv(1024) == 'READY':
                conn.send('READY')

            # Handle requests from the controller
            cmd = conn.recv(1024)
            if cmd != 'TEARDOWN':
                # Create a thread to print texts from server
                thread1 = threading.Thread(target=server_listener, args=(s2,))
                thread1.start()
            while cmd != 'TEARDOWN':
                s2.send(cmd)
                cmd = conn.recv(1024)
            s2.send(cmd)
            thread1.join()
            s2.close()
            print '----- Rendering Ended -----'

        else:
            print 'SETUP has not been received'

        print 'Closing connection!'
        conn.close()

    except IOError:

        print IOError
        conn.close()
        s1.close()
