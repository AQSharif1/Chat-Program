import socket;
import sys;
import threading;
username = input("Enter your username: ");

if len(sys.argv) > 1:
    port = int(sys.argv[1]);
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
client.connect(('127.0.0.1', port));

def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            if message == 'User':
                client.send(username.encode())
    

            elif message == 'Exit':
                client.close()
                exit()
            else:
                print(message);
        except Exception:
            print("error!");
            client.close();
            break


def write():
    while True:
        message = input();
        client.send(message.encode());

receive_thread = threading.Thread(target=receive);
receive_thread.start();

write_thread = threading.Thread(target=write);
write_thread.start();