import socket;
import threading;
import sys;

host = '127.0.0.1';
if len(sys.argv) > 1:
    port = int(sys.argv[1]);

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port));
server.listen();

clients = [];
usernames = [];
dict_available_users = {}

def readfile():
    try:
        file = open("dataFile.txt").readlines()
        for line in file:
            line = line.strip().split(",")
            dict_available_users[line[0]] = line[1]
    except Exception:
        pass

def updateTxtFile():
    file = open("dataFile.txt", "w")
    for key, value in dict_available_users.items():
        file.write(key + "," + value + "\n")
    file.close()
def send_to_all(msg):
    for client in clients:
        client.send(msg)


def send_dm(username, msg):
    for i, user in enumerate(usernames):
        if user == username:
            client = clients[i]
            client.send(msg.encode())
            return True
    return False


def remove_client(client):
    index = clients.index(client);
    clients.pop(index);
    client.close();
    username = usernames[index]
    send_to_all('{} left!'.format(str(username)).encode());
    usernames.pop(index);


def handle(client):
    while True:
        index = clients.index(client);
        try:
            client.send("\nChoose an option: PM (Private Message), DM (Direct Message), Exit".encode());
            choice = client.recv(1024).decode().upper();

            if choice.upper() in ["PM", "DM", "Exit"]:
                if choice == "PM":
                    client.send("Type message: ".encode())
                    message = client.recv(1024).decode()

                    full_message = usernames[index] + ": " + message
                    send_to_all(full_message.encode())

                elif choice == "DM":
                    message = "Online user: " + ", ".join(usernames) + "\nChoose a username: "
                    client.send(message.encode())
                    username = client.recv(1024).decode()
                    if username in usernames:
                        client.send("Type a message: ".encode())
                        message = client.recv(1024).decode()
                        full_message = usernames[index] + ": " + message
                        send_dm(username, full_message)
                    else:
                        client.send("That User is not currently online".encode())
                elif choice == "Exit":
                    client.send("Exit".encode())
                    
                    remove_client(client);
                    
                    break
            else:
                client.send("Invalid Choice. Choose again Please".encode());
        except Exception as e:
            print(e);
           
            remove_client(client);
            break


def receive():
    while True:
        # Accept Connection to the client and server
        client, address = server.accept();
        print("Connected with {}".format(str(address)));

        client.send('User'.encode());
        username = client.recv(1024).decode();
        if username in dict_available_users.keys():
            print("Password authentication...");
            client.send("Existing User: Enter User Password".encode());
            password = client.recv(1024).decode();
            try:
                if password == dict_available_users.get(username):
                    usernames.append(username);
                    clients.append(client);

                    print("Username is {}".format(username))
                    send_to_all("{} Logged in!".format(username).encode());
                    client.send('\nConnected to the server!'.encode());
            
                    thread = threading.Thread(target=handle, args=(client,));
                    thread.start();
                else:
                    while password !=dict_available_users.get(username):
                        client.send("Incorrect password entered. Try Again!".encode());
                        password = client.recv(1024).decode();    
                        
                        if password == dict_available_users.get(username):
                             usernames.append(username);
                             clients.append(client);                

                             print("Username is {}".format(username))
                             send_to_all("{} Logged in!".format(username).encode());
                             client.send('\nConnected to the server!'.encode());
            
                             thread = threading.Thread(target=handle, args=(client,));
                             thread.start();
            except Exception as e:
                print(e);
                
            
        else:
            client.send("New User: Create a password".encode());
            password = client.recv(1024).decode();
            dict_available_users[username] = password;
            usernames.append(username);
            clients.append(client);

            print("Username is {}".format(username));
            send_to_all("{} joined!".format(username).encode());
            client.send('\nConnected to the server!'.encode());
            updateTxtFile();
            newThread = threading.Thread(target=handle, args=(client,));
            newThread.start();

print("Server is ready...");
readfile();
receive();