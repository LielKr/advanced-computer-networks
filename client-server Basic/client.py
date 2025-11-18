import socket

my_socket=socket.socket()                            # אובייקט socket בשם my_socket
my_socket.connect(('127.0.0.1',8200))  #יצרנו חיבור עם התוכנה (שהיא בשרת שבכתובת 127.0.0.1) שמאזינה בפורט 8200

my_socket.send('hello there, im sending from thr client'.encode())       #דעי שהודעה מוצפנת היא מסוג byte ולא int...
length = int(my_socket.recv(3).decode())
data = my_socket.recv(length).decode()
print('this is what the server send ( i got it with recv.. ): \n'+data)

my_socket.close()

#        אז מה היה לנו פה:
#1. פתיחת socket וחיבור ל IP ו PORT
#             2. שליחת הודעה עם send
#        3. קבלת הודעה מהשרת עם recv
#           4. הדפסה וסגירת ה socket
