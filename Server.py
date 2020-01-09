from socket import *
import os

# Create sockets for controller/renderer to connect to
PORT = 2001
try:
    s = socket(AF_INET, SOCK_STREAM)
except error as err:
    print 'socket creation failed with error %s' % (err)
s.bind(('', PORT))
s.listen(1)

while 1:
    print '\nServer Listening...'
    conn, addr = s.accept()
    print '\nConnected by', addr

    try:

        # Controller Request
        request = conn.recv(1024)
        if request == 'LIST':
            print '>>> sending list of text files'
            #for file in os.listdir('/Users/farhanr8/PycharmProjects/Mininet'):
            for file in os.listdir('/home/mininet/CS4390/Project'):
                if file.endswith('.txt'):
                    conn.send(file[:-4])
                    while 1:
                        if conn.recv(1024) == 'OK':
                            break
            conn.send('EOL')

        # Handle renderer request and stream accordingly
        elif request.split()[0] == 'SETUP':
            print '>>> Opening file requested'
            fileNum = request.split()[1]
            curNum = 1
            #for file in os.listdir('/Users/farhanr8/PycharmProjects/Mininet'):
            for file in os.listdir('/home/mininet/CS4390/Project'):
                if file.endswith('.txt') and curNum == int(fileNum):
                    f = open(file, 'r')
                    if f.mode == 'r':
                        conn.send('READY')
                        break
                elif file.endswith('.txt'):
                    curNum += 1

            # Waiting for renderer to play
            req = conn.recv(1024)
            while 'TEARDOWN' not in req:
                if 'PLAY' in req:
                    if 'REPLAY' not in req:
                        print '>>> playing'
                    f1 = f.readlines()
                    count = 0

                    for x in f1:
                        count += 1
                        conn.send(x)
                        req = conn.recv(1024)
                        if req == 'OK':
                            pass
                        if 'PAUSE' in req:
                            print '>>> pausing'
                            while 'PLAY' not in req and 'TEARDOWN' not in req:
                                req = conn.recv(1024)
                            if 'REPLAY' not in req and 'PlAy' in req:
                                print '>>> playing'
                        if 'REPLAY' in req:
                            print '>>> replaying'
                            f.seek(0)
                            break
                        if 'TEARDOWN' in req:
                            conn.send('TEARDOWN')
                            conn.recv(1024)
                            break

                    if count == len(f1):
                        conn.send('\nEND OF FILE: Please TEARDOWN or REPLAY\n')
                        req = conn.recv(1024)
                        while 'TEARDOWN' not in req and 'REPLAY' not in req:
                            req = conn.recv(1024)
                        if 'REPLAY' in req:
                            f.seek(0)
                        elif 'TEARDOWN' in req:
                            conn.send('TEARDOWN')
                            conn.recv(1024)
                else:
                    req = conn.recv(1024)


            print '>>> exiting'
            f.close()

        else:
            print 'LIST or SETUP has not been received'

        print 'Closing connection!'
        conn.close()

    except IOError:

        conn.close()
        s.close()
