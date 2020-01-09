from socket import *

while 1:
    msg = ('To view text files available for streaming please enter '
           'the command LIST')
    print(msg)
    userCmd = raw_input()
    if userCmd != 'LIST':
        print 'Invalid input: Try again!\n'
        continue

    # Server connection and commands
    server_port = 2001
    #server_ip = '192.168.1.88'
    server_ip = '10.0.0.1'
    try:
        s1 = socket(AF_INET, SOCK_STREAM)
    except error as err:
        print 'socket creation failed with error %s' % (err)
    s1.connect((server_ip, server_port))
    s1.send('LIST')
    file_name = s1.recv(1024)
    num = 1
    while file_name != 'EOL':
        print ('%s) %s' % (num, file_name))
        s1.send('OK')
        file_name = s1.recv(1024)
        num += 1
    s1.close()

    print '\nPlease select a text to read by entering its corresponding number:'
    book_num = int(input())
    while book_num < 1 or book_num > num:
        print 'Invalid number! Try again:'
        book_num = int(input())

    # Renderer connection and commands
    renderer_port = 2002
    #renderer_ip = '192.168.1.88'
    renderer_ip = '10.0.0.2'
    try:
        s2 = socket(AF_INET, SOCK_STREAM)
    except error as err:
        print 'socket creation failed with error %s' % (err)
    s2.connect((renderer_ip, renderer_port))
    s2.send('SETUP ' + str(book_num))
    reply = s2.recv(1024)
    if reply == 'READY':
        print'Please enter a command: PLAY PAUSE REPLAY TEARDOWN'
        userCmd = raw_input()
        s2.send(userCmd)
        while userCmd != 'TEARDOWN':
            userCmd = raw_input()
            s2.send(userCmd)
    s2.close()







