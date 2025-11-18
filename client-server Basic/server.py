import socket

server_socket = socket.socket()
server_socket.bind(("0.0.0.0",8200))
server_socket.listen()

print("Server is up and listening")
(client_socket,client_adress) = server_socket.accept()  # יקפא עד שיתקבל חיבור כלשהו בשרת
print("Client is connected successfully")

data = client_socket.recv(1024).decode()
print("client send this:\n" + data + '\n')
print("lets send to the client-")
client_socket.send("hi, its the server, thank you for your data i recieved".encode())

client_socket.close()
server_socket.close()
